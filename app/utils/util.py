import os
import requests
import json
import zipfile

from te_schemas.land_cover import (
    LCLegendNesting,
    LCTransitionMeaningDeg,
    LCTransitionDefinitionDeg,
    LCTransitionMatrixDeg,
)
from django.conf import settings

from .logger import log


def get_trans_matrix():
    """
    Get the default land cover transition matrix.

    This function is deprecated. Use te_schemas to create your own
    LCTransitionDefinitionDeg instances with appropriate data.
    The UNCCD default data should be provided by te_schemas package.
    """
    raise NotImplementedError(
        "get_trans_matrix() is deprecated. Use te_schemas.land_cover.LCTransitionDefinitionDeg "
        "with appropriate UNCCD default data from te_schemas package."
    )


def read_lc_matrix_file(f):
    """
    Read land cover matrix file using te_schemas.

    This function is deprecated. Use te_schemas.land_cover.LCTransitionDefinitionDeg.Schema().loads()
    directly with appropriate data from te_schemas package instead of local files.
    """
    raise NotImplementedError(
        "read_lc_matrix_file() is deprecated. Use te_schemas.land_cover.LCTransitionDefinitionDeg.Schema().loads() "
        "directly with data from te_schemas package instead of local files."
    )


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
            meaning = matrix.definitions.meaning_by_transition(
                initial_class, final_class
            )
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
                code = '<input type="text" value="?" class="lc-input unknown"/>'
            tbody += "<td>" + code + "</td>"
        tbody += "</tr>"
    tbody += "</tbody>"
    return tbody


def table_to_matrix(tdata, matrix=None, nesting=None):
    """
    Convert table data to transition matrix.

    This function requires proper te_schemas LCTransitionDefinitionDeg and LCLegendNesting
    instances to be provided. Use te_schemas package to create appropriate instances
    with UNCCD default data.
    """
    if nesting is None:
        raise ValueError(
            "nesting parameter is required. Use te_schemas.land_cover.LCLegendNesting "
            "with appropriate UNCCD/ESA default data from te_schemas package."
        )
    if matrix is None:
        raise ValueError(
            "matrix parameter is required. Use te_schemas.land_cover.LCTransitionDefinitionDeg "
            "with appropriate UNCCD default data from te_schemas package."
        )

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
    Get land cover nesting.

    This function is deprecated. Use te_schemas to create your own
    LCLegendNesting instances with appropriate data.
    The UNCCD/ESA default data should be provided by te_schemas package.
    """
    if nesting is not None:
        return LCLegendNesting.Schema().loads(nesting)

    raise NotImplementedError(
        "get_lc_nesting() with default data is deprecated. Use te_schemas.land_cover.LCLegendNesting "
        "with appropriate UNCCD/ESA default data from te_schemas package."
    )


def read_lc_nesting_file(f):
    """
    Read land cover nesting file using te_schemas.

    This function is deprecated. Use te_schemas.land_cover.LCLegendNesting.Schema().loads()
    directly with appropriate data from te_schemas package instead of local files.
    """
    raise NotImplementedError(
        "read_lc_nesting_file() is deprecated. Use te_schemas.land_cover.LCLegendNesting.Schema().loads() "
        "directly with data from te_schemas package instead of local files."
    )


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
