from typing import Any, List, Optional
from enum import Enum
import math
from typing_extensions import Final
import copy


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    copied_rows = copy.deepcopy(rows)
    if labels is not None:
        label_copy = copy.deepcopy(labels)
        copied_rows.append(label_copy)
    bar_positions = get_width_of_table(copied_rows)
    modified_rows = modify_lists_for_printing(
        copied_rows, bar_positions, centered)
    separatorGenerator = SeparatorGenerator(bar_positions)
    if labels is not None:
        result = "\n".join(
            ["│ "+' │ '.join(row)+" │" for row in modified_rows[:-1]])
        return cat_strings((separatorGenerator.createSeparator(TYPE.HEADER), "│ "+' │ '.join(modified_rows[-1])+" │", separatorGenerator.createSeparator(TYPE.MIDDLE), result, separatorGenerator.createSeparator(TYPE.FOOTER)))
    else:
        result = "\n".join(
            ["│ "+' │ '.join(row)+" │" for row in modified_rows])
        return cat_strings((separatorGenerator.createSeparator(TYPE.HEADER), result, separatorGenerator.createSeparator(TYPE.FOOTER)))


# Helper methods

def get_width_of_table(rows: List[List[Any]]) -> int:
    number_of_cols = len(rows[0])
    position_of_bar = [-1 for i in range(number_of_cols)]
    for col in range(number_of_cols):
        for row in rows:
            if len(str(row[col])) > position_of_bar[col]:
                position_of_bar[col] = len(str(row[col]))
    return position_of_bar


def modify_lists_for_printing(rows: List[List[Any]], positions, centered: bool) -> List[List[Any]]:
    mod_rows = list(rows)
    for id in range(len(rows)):
        for i in range(len(rows[id])):
            diff = positions[i]-len(str(rows[id][i]))
            if centered:
                pre = math.floor(diff/2)
                post = diff - pre
                mod_rows[id][i] = " "*pre + str(mod_rows[id][i]) + " "*post
            else:
                mod_rows[id][i] = str(mod_rows[id][i])+" "*diff
    return mod_rows


def cat_strings(*args):
    result = ""
    for arg in args[0]:
        result = result+arg+"\n"

    return result

# For generating upper and lower bounding box and the separator between header and other rows


class TYPE(Enum):
    HEADER = 1
    MIDDLE = 2
    FOOTER = 3


SIDE_SPACE: Final = 2


class SeparatorGenerator:
    def __init__(self, pos: List) -> None:
        self.pos = pos

    def createSeparator(self, separtor: TYPE):
        if separtor == TYPE.HEADER:
            return self._makeGeneralSeparator(start=u"┌", end=u"┐", col_sep=u"┬", joiner=u"─")
        elif separtor == TYPE.MIDDLE:
            return self._makeGeneralSeparator(start=u"├", end=u"┤", col_sep=u"┼", joiner=u"─")
        elif separtor == TYPE.FOOTER:
            return self._makeGeneralSeparator(start=u"└", end=u"┘", col_sep=u"┴", joiner=u"─")

    def _makeGeneralSeparator(self, **kwargs):
        temp_list = []
        temp_list.append(kwargs.get("start"))
        for i in range(len(self.pos)):
            temp_list.append(kwargs.get("joiner")*(self.pos[i]+SIDE_SPACE))
            if(i != (len(self.pos)-1)):
                temp_list.append(kwargs.get("col_sep"))
        temp_list.append(kwargs.get("end"))
        return ''.join(temp_list)
