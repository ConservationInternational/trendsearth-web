import os
import requests
import json
import zipfile

from marshmallow.exceptions import ValidationError
from django.conf import settings

from .schemas_compat import (
    LCLegendNesting, 
    LCTransitionMeaningDeg,
    LCTransitionDefinitionDeg,
    LCTransitionMatrixDeg,
    get_default_land_cover_matrix,
    get_default_land_cover_nesting,
    TE_SCHEMAS_AVAILABLE,
)
from .logger import log


def get_trans_matrix():
    """
    Get the default land cover transition matrix.
    
    Prefer te_schemas built-in data over local files when available.
    """
    # First try to get from te_schemas compatibility layer
    matrix = get_default_land_cover_matrix()
    if matrix is not None:
        return matrix
    
    # Fallback to old method if compatibility layer fails
    return read_lc_matrix_file(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data", 
            "land_cover_transition_matrix_unccd.json",
        )
    )


def read_lc_matrix_file(f):
    """
    Read land cover matrix file using te_schemas when available.
    
    This function is deprecated and should be replaced by using
    te_schemas built-in default matrices.
    """
    try:
        with open(f) as matrix_file:
            if TE_SCHEMAS_AVAILABLE:
                matrix = LCTransitionDefinitionDeg.Schema().loads(matrix_file.read())
            else:
                # Fallback to simple JSON loading if te_schemas not available
                matrix = json.load(matrix_file)
    except (ValidationError, json.JSONDecodeError) as e:
        log(f"Error loading land cover transition matrix from {f}: {e}")
        return None
    else:
        log(f"Loaded land cover transition matrix definition from {f}")
        return matrix


def matrix_to_table(matrix=None):
    if not matrix:
        matrix = get_trans_matrix()
    rows = len(matrix.legend.key)
    cols = len(matrix.legend.key)
    horizontalHeaderLabels = [c.name_short for c in matrix.legend.key]
    tbody = "<tbody><tr><th></th>"
    for c in matrix.legend.key:
        tbody += "<th>" + c.name_short + "</th>"
    tbody += "</tr>"
    for row in range(0, rows):
        initial_class = matrix.legend.key[row]

        tbody += "<tr>"
        tbody += "<th>" + horizontalHeaderLabels[row] + "</th>"
        for col in range(0, cols):
            final_class = matrix.legend.key[col]
            meaning = matrix.definitions.meaningByTransition(initial_class, final_class)
            if meaning == "stable":
                code = '<input type="text" value="0" class="lc-input stable"/>'
            elif meaning == "degradation":
                code = '<input type="text" value="-" class="lc-input degradation"/>'
            elif meaning == "improvement":
                code = '<input type="text" value="+" class="lc-input improvement"/>'
            else:
                log(
                    'unrecognized transition meaning "{}" when setting transition matrix'.format(
                        meaning
                    )
                )
            tbody += "<td>" + code + "</td>"
        tbody += "</tr>"
    tbody += "</tbody>"
    return tbody


def table_to_matrix(tdata, matrix=None, nesting=None):
    if nesting is None:
        nesting = get_lc_nesting()
    if matrix is None:
        matrix = get_trans_matrix()
    rows = len(matrix.legend.key)
    cols = len(matrix.legend.key)

    transitions = []
    for row in range(0, rows):
        for col in range(0, cols):
            val = tdata[row][col]
            if val == "" or val == "0":
                meaning = "stable"
            elif val == "-":
                meaning = "degradation"
            elif val == "+":
                meaning = "improvement"
            else:
                log(
                    'unrecognized value "{}" when reading transition meaning from cellWidget'.format(
                        val
                    )
                )
                raise ValueError(
                    'unrecognized value "{}" when reading transition meaning from cellWidget'.format(
                        val
                    )
                )
            transitions.append(
                LCTransitionMeaningDeg(
                    nesting.parent.key[row], nesting.parent.key[col], meaning
                )
            )
    return LCTransitionDefinitionDeg(
        legend=nesting.parent,
        name="Land cover transition definition matrix",
        definitions=LCTransitionMatrixDeg(
            name="Degradation matrix", transitions=transitions
        ),
    )


def get_lc_nesting(nesting=None):
    """
    Get land cover nesting, preferring te_schemas built-in data.
    
    This function is deprecated and should be replaced by using
    te_schemas built-in default nesting.
    """
    if nesting is None:
        # Try to get from te_schemas compatibility layer first
        default_nesting = get_default_land_cover_nesting()
        if default_nesting is not None:
            if TE_SCHEMAS_AVAILABLE:
                return default_nesting
            else:
                # Convert JSON to expected format for backward compatibility
                return default_nesting
        
        # Fallback to local file
        nesting = read_lc_nesting_file(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "data",
                "land_cover_nesting_unccd_esa.json",
            )
        )
    else:
        if TE_SCHEMAS_AVAILABLE:
            nesting = LCLegendNesting.Schema().loads(nesting)
        else:
            nesting = json.loads(nesting) if isinstance(nesting, str) else nesting
    return nesting


def read_lc_nesting_file(f):
    """
    Read land cover nesting file using te_schemas when available.
    
    This function is deprecated and should be replaced by using
    te_schemas built-in default nesting.
    """
    try:
        with open(f) as nesting_file:
            if TE_SCHEMAS_AVAILABLE:
                nesting = LCLegendNesting.Schema().loads(nesting_file.read())
            else:
                # Fallback to simple JSON loading if te_schemas not available
                nesting = json.load(nesting_file)
    except (ValidationError, json.JSONDecodeError) as e:
        log(f"Error loading land cover legend nesting definition from {f}: {e}")
        return None
    else:
        log("Loaded land cover legend nesting definition from {}".format(f))
        return nesting


def url_exists(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        return True
    else:
        return False


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_styles():
    styles = {}
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data", "styles.json"
        ),
        encoding="utf-8",
    ) as script_file:
        styles = json.load(script_file)

    return styles


def get_file_extension(file_path):
    split_path = os.path.basename(file_path).split(".")
    if len(split_path) > 1:
        return (split_path[-1]).lower()


def extract_zipped_file(file_path):
    archive_path = settings.MEDIA_ROOT
    filelist = []
    if os.path.exists(file_path):
        try:
            with zipfile.ZipFile(file_path, "r") as z:
                filelist = [
                    settings.MEDIA_ROOT + os.sep + f.filename for f in z.filelist
                ]
                z.extractall(archive_path)
        except Exception as e:
            print(e)
    return filelist
