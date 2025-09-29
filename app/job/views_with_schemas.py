"""
Example integration of marshmallow schemas with job processing.

This demonstrates how the existing process functions could be refactored
to use schema validation instead of manual parameter extraction.
"""

import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from marshmallow import ValidationError

from account import models as accountmodels
from core import models as coremodels
from utils import conf
from utils.api import Api
from utils.logger import log
from utils.util import table_to_matrix, get_trans_matrix
from te_schemas.land_cover import LCTransitionDefinitionDeg

from .schema_utils import validate_and_transform_parameters, get_schema_for_script

# Default CRS (same as in original views.py)
CRS = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'


def process_land_cover_with_schema(request):
    """
    Example of processing land cover parameters using marshmallow schema validation.

    This replaces the manual parameter extraction with schema-based validation.
    """
    try:
        # Validate parameters using schema
        validated_data = validate_and_transform_parameters("land-cover", request)[0]

        # Process transition matrix data using te_schemas (consistent with original code)
        form_data = json.loads(validated_data["tdata"])
        matrix = table_to_matrix(form_data)
        matrix = LCTransitionDefinitionDeg.Schema().dumps(matrix)

        # Get legend nesting (same logic as original)
        agg_classes = coremodels.UserAggregationClass.objects.filter(user=request.user)
        if agg_classes.count() == 0:
            agg_classes = coremodels.UserAggregationClass.objects.filter(
                user_id=None
            ).exclude(inputclass__code="-32768")

        legend_nesting = get_trans_matrix(agg_classes)

        # Build payload with validated data
        payload = {
            "geojsons": validated_data["geojsons"],
            "crs": validated_data["crs"],
            "crosses_180th": validated_data["crosses_180th"],
            "task_name": validated_data["task_name"],
            "task_notes": validated_data["task_notes"],
            "year_initial": validated_data["initial_year_de"],
            "year_final": validated_data["target_year_de"],
            "legend_nesting": legend_nesting,
            "trans_matrix": json.loads(matrix),
        }

        return [payload]

    except ValidationError as e:
        log(f"Parameter validation failed: {e.messages}")
        raise
    except Exception as e:
        log(f"Error processing land cover parameters: {e}")
        raise


def process_drought_vulnerability_with_schema(request):
    """
    Example of processing drought vulnerability parameters using schema validation.
    """
    try:
        # Validate parameters using schema
        validated_data = validate_and_transform_parameters(
            "drought-vulnerability", request
        )[0]

        # Use predefined datasets (same as original)
        population_dataset_name = "Gridded Population Count"
        population_dataset = conf.REMOTE_DATASETS["WorldPop"][population_dataset_name]

        spi_dataset_name = "GPCC V6 (Global Precipitation Climatology Centre)"
        spi_dataset = conf.REMOTE_DATASETS["SPI"][spi_dataset_name]

        # Build payload with validated data
        payload = {
            "geojsons": validated_data["geojsons"],
            "crs": validated_data["crs"],
            "crosses_180th": validated_data["crosses_180th"],
            "task_name": validated_data["task_name"],
            "task_notes": validated_data["task_notes"],
            "year_initial": validated_data["year_initial"],
            "year_final": validated_data["year_final"],
            "population": {
                "asset": population_dataset["GEE Dataset"],
                "source": population_dataset_name,
            },
            "spi": {
                "asset": spi_dataset["GEE Dataset"],
                "source": spi_dataset_name,
                "lag": validated_data["lag_cb"],
            },
            "land_cover": {
                "asset": "users/geflanddegradation/toolbox_datasets/lcov_esacc_1992_2022",
                "source": "ESA CCI",
            },
        }

        return [payload]

    except ValidationError as e:
        log(f"Parameter validation failed: {e.messages}")
        raise
    except Exception as e:
        log(f"Error processing drought vulnerability parameters: {e}")
        raise


@login_required
def ajax_run_job_with_schemas(request):
    """
    Example of how the main job processing function could be refactored
    to use schema validation for all script types.
    """
    if not request.POST:
        return JsonResponse({"error": "No POST data provided"}, status=400)

    try:
        algo_name = request.POST.get("algo")
        if not algo_name:
            return JsonResponse({"error": "Algorithm name not provided"}, status=400)

        # Check if we have a schema for this algorithm
        schema = get_schema_for_script(algo_name)
        if not schema:
            return JsonResponse(
                {"error": f"No schema available for algorithm: {algo_name}"}, status=400
            )

        # Get the script
        script = accountmodels.Script.objects.get(name=algo_name, run_mode="remote")

        # Validate parameters and get payloads
        try:
            payloads = validate_and_transform_parameters(algo_name, request)
        except ValidationError as e:
            return JsonResponse(
                {"error": "Parameter validation failed", "details": e.messages},
                status=400,
            )

        # Submit jobs using validated payloads
        api = Api(token=request.session["bearer_token"])
        job_responses = []

        for payload in payloads:
            if payload.get("crs") == "None":
                payload["crs"] = CRS

            url_fragment = "/api/v1/script/" + script.uid + "/run"
            response = api.call_api(url_fragment, "post", payload, use_token=True)

            if response and response.get("data"):
                job_responses.append(response["data"])

        return JsonResponse(
            {
                "success": True,
                "jobs": job_responses,
                "message": f"Successfully submitted {len(job_responses)} jobs",
            }
        )

    except accountmodels.Script.DoesNotExist:
        return JsonResponse({"error": f"Script not found: {algo_name}"}, status=404)
    except Exception as e:
        log(f"Error in ajax_run_job_with_schemas: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)


def get_schema_info(request):
    """
    API endpoint to get schema information for dynamic GUI generation.
    """
    script_name = request.GET.get("script")
    if not script_name:
        return JsonResponse({"error": "script parameter required"}, status=400)

    try:
        from .schema_utils import get_schema_fields_for_gui, get_schema_description

        fields = get_schema_fields_for_gui(script_name)
        if not fields:
            return JsonResponse(
                {"error": f"No schema found for script: {script_name}"}, status=404
            )

        description = get_schema_description(script_name)

        return JsonResponse(
            {"script": script_name, "description": description, "fields": fields}
        )

    except Exception as e:
        log(f"Error getting schema info: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)
