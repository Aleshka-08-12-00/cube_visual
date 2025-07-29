from fastapi import APIRouter, HTTPException, Query
from ..adomd import fetch_limited

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("/cubes")
def cubes():
    q = "SELECT CUBE_NAME FROM $SYSTEM.MDSCHEMA_CUBES WHERE CUBE_SOURCE=1 ORDER BY CUBE_NAME"
    cols, rows = fetch_limited(q, 0)
    return [{"cube_name": r[0]} for r in rows]


@router.get("/measures")
def measures(cube: str = Query(...)):
    q = f"SELECT MEASURE_NAME, MEASURE_UNIQUE_NAME, MEASUREGROUP_NAME, DEFAULT_FORMAT_STRING FROM $SYSTEM.MDSCHEMA_MEASURES WHERE CUBE_NAME='{cube}' ORDER BY MEASURE_NAME"
    cols, rows = fetch_limited(q, 0)
    return [
        {
            "measure_name": r[0],
            "measure_unique_name": r[1],
            "measure_group": r[2],
            "format_string": r[3],
        }
        for r in rows
    ]


@router.get("/dimensions")
def dimensions(cube: str = Query(...)):
    cube_escaped = cube.replace("'", "''")
    q_h = f"""
SELECT DIMENSION_UNIQUE_NAME, HIERARCHY_UNIQUE_NAME, DIMENSION_TYPE, IS_VIRTUAL
FROM $SYSTEM.MDSCHEMA_HIERARCHIES
WHERE CUBE_NAME = '{cube_escaped}'
"""
    cols_h, rows_h = fetch_limited(q_h, 0)
    rows_h = [dict(zip(cols_h, r)) for r in rows_h]

    # Filter out virtual hierarchies and measure dimensions
    rows_h = [
        r for r in rows_h if not r["IS_VIRTUAL"] and r["DIMENSION_TYPE"] != 2
    ]

    uniques = []
    seen = set()
    for r in rows_h:
        u = r["DIMENSION_UNIQUE_NAME"]
        if u not in seen:
            seen.add(u)
            uniques.append(u)

    q_d = (
        f"SELECT [DIMENSION_UNIQUE_NAME],[DIMENSION_NAME],[DIMENSION_CAPTION],[DIMENSION_IS_VISIBLE] "
        f"FROM $SYSTEM.MDSCHEMA_DIMENSIONS "
        f"WHERE [CUBE_NAME]='{cube_escaped}'"
    )
    _, rows_d = fetch_limited(q_d, 0)
    meta = {
        r[0]: {"name": r[1], "caption": r[2], "visible": bool(r[3])} for r in rows_d
    }

    dims = []
    for u in uniques:
        m = meta.get(u, {})
        name = m.get("name") or m.get("caption") or u
        dims.append({"dimension_name": name, "dimension_unique_name": u})
    return dims


@router.get("/hierarchies")
def hierarchies(cube: str = Query(...), dimension_unique_name: str | None = None):
    cube_escaped = cube.replace("'", "''")
    where = ""
    if dimension_unique_name:
        dim_escaped = dimension_unique_name.replace("'", "''")
        where = f" AND [DIMENSION_UNIQUE_NAME]='{dim_escaped}'"
    q = (
        "SELECT [HIERARCHY_NAME],[HIERARCHY_UNIQUE_NAME],[DIMENSION_UNIQUE_NAME],[DIMENSION_TYPE],[HIERARCHY_IS_VISIBLE] "
        "FROM $SYSTEM.MDSCHEMA_HIERARCHIES "
        f"WHERE [CUBE_NAME]='{cube_escaped}'{where} "
        "ORDER BY [HIERARCHY_NAME]"
    )
    cols, rows = fetch_limited(q, 0)
    vis_idx = cols.index("HIERARCHY_IS_VISIBLE")
    type_idx = cols.index("DIMENSION_TYPE")
    rows = [r for r in rows if r[vis_idx] and r[type_idx] != 2]
    return [
        {
            "hierarchy_name": r[0],
            "hierarchy_unique_name": r[1],
            "dimension_unique_name": r[2],
        }
        for r in rows
    ]


@router.get("/levels")
def levels(cube: str = Query(...), hierarchy_unique_name: str = Query(...)):
    q = f"SELECT LEVEL_NAME, LEVEL_UNIQUE_NAME, LEVEL_NUMBER FROM $SYSTEM.MDSCHEMA_LEVELS WHERE CUBE_NAME='{cube}' AND HIERARCHY_UNIQUE_NAME='{hierarchy_unique_name}' ORDER BY LEVEL_NUMBER"
    cols, rows = fetch_limited(q, 0)
    return [
        {"level_name": r[0], "level_unique_name": r[1], "level_number": r[2]}
        for r in rows
    ]


@router.get("/members")
def members(
    cube: str = Query(...),
    level_unique_name: str = Query(...),
    search: str | None = None,
    limit: int = 1000,
):
    like = ""
    if search:
        s = search.replace("'", "''")
        like = f" AND UPPER(MEMBER_CAPTION) LIKE UPPER('%{s}%')"
    q = f"SELECT MEMBER_CAPTION, MEMBER_UNIQUE_NAME FROM $SYSTEM.MDSCHEMA_MEMBERS WHERE CUBE_NAME='{cube}' AND LEVEL_UNIQUE_NAME='{level_unique_name}'{like} ORDER BY MEMBER_CAPTION"
    cols, rows = fetch_limited(q, limit)
    return [{"caption": r[0], "unique_name": r[1]} for r in rows]
