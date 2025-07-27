from typing import List, Optional

def _brace_join(items: List[str]) -> str:
    return "{%s}" % (", ".join(items) if items else "")

def _crossjoin(sets: List[str]) -> str:
    if not sets:
        return "{}"
    if len(sets) == 1:
        return sets[0]
    expr = sets[0]
    for s in sets[1:]:
        expr = f"NonEmptyCrossJoin({expr}, {s})"
    return expr

def build_mdx(cube: str, measures: List[str], row_sets: List[str], col_sets: List[str], slicers: Optional[List[str]] = None) -> str:
    m = _brace_join(measures)
    rows_expr = _crossjoin(row_sets) if row_sets else "{}"
    cols_expr = _crossjoin(col_sets) if col_sets else m
    slicer = ""
    if slicers:
        slicer = " WHERE (%s)" % ", ".join(slicers)
    mdx = f"SELECT NON EMPTY {cols_expr} ON COLUMNS, NON EMPTY {rows_expr} ON ROWS FROM [{cube}]{slicer}"
    return mdx
