import os
from marshmallow.exceptions import ValidationError
from te_schemas.land_cover import (
    LCLegend,
    LCLegendNesting,
    LCClass,
    LCTransitionMeaningDeg,
    LCTransitionDefinitionDeg,
    LCTransitionMatrixDeg
)

from .logger import log


def get_trans_matrix():
    return read_lc_matrix_file(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'land_cover_transition_matrix_unccd.json'
        )
    )


def read_lc_matrix_file(f):

    try:
        with open(f) as matrix_file:
            matrix = LCTransitionDefinitionDeg.Schema().loads(
                matrix_file.read()
            )
    except ValidationError as e:
        log(f'Error loading land cover transition matrix from {f}: {e}')
        return None
    else:
        log(f'Loaded land cover transition matrix definition from {f}')
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
            meaning = matrix.definitions.meaningByTransition(
                initial_class, final_class)
            if meaning == 'stable':
                code = '<input type="text" value="0" class="lc-input stable"/>'
            elif meaning == 'degradation':
                code = '<input type="text" value="-" class="lc-input degradation"/>'
            elif meaning == 'improvement':
                code = '<input type="text" value="+" class="lc-input improvement"/>'
            else:
                log('unrecognized transition meaning "{}" when setting transition matrix'.format(
                    meaning))
            tbody += "<td>" + code + "</td>"
        tbody += "</tr>"
    tbody += "</tbody>"
    return tbody


def table_to_matrix(matrix=None, nesting=None):
    # Extract trans_matrix from the QTableWidget
    if nesting is None:
        nesting = get_lc_nesting()
    if matrix is None:
        matrix = get_trans_matrix()
    rows = len(matrix.legend.key)
    cols = len(matrix.legend.key)

    transitions = []
    for row in range(0, rows):
        for col in range(0, cols):
            # val = self.deg_def_matrix.cellWidget(row, col).text()
            val = "0"
            if val == "" or val == "0":
                meaning = "stable"
            elif val == "-":
                meaning = "degradation"
            elif val == "+":
                meaning = "improvement"
            else:
                log('unrecognized value "{}" when reading transition meaning from cellWidget'.format(
                    val))
                raise ValueError(
                    'unrecognized value "{}" when reading transition meaning from cellWidget'.format(val))
            transitions.append(
                LCTransitionMeaningDeg(
                    nesting.parent.key[row],
                    nesting.parent.key[col],
                    meaning
                )
            )
    return LCTransitionDefinitionDeg(
        legend=nesting.parent,
        name="Land cover transition definition matrix",
        definitions=LCTransitionMatrixDeg(
            name="Degradation matrix",
            transitions=transitions
        )
    )


def get_lc_nesting(nesting=None):

    if nesting is None:
        nesting = read_lc_nesting_file(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'land_cover_nesting_unccd_esa.json'
            )
        )
    else:
        nesting = LCLegendNesting.Schema().loads(nesting)
    return nesting


def read_lc_nesting_file(f):
    try:
        with open(f) as nesting_file:
            nesting = LCLegendNesting.Schema().loads(nesting_file.read())
    except ValidationError as e:
        log("Error loading land cover legend "
            f"nesting definition from {f}: {e}")

    else:
        log(u'Loaded land cover legend nesting definition from {}'.format(f))
        return nesting
