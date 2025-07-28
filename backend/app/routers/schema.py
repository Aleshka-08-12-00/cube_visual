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
    return [{"measure_name": r[0], "measure_unique_name": r[1], "measure_group": r[2], "format_string": r[3]} for r in rows]

@router.get("/dimensions")
def dimensions(cube: str = Query(...)):
    # DIMENSION_UNIQUE_NAME is not available in MDSCHEMA_DIMENSIONS on some
    # servers which results in a syntax error when querying this rowset.
    # Instead, fetch distinct dimension information from the hierarchies
    # rowset which always exposes the unique name.
    q = (
        f"SELECT DIMENSION_NAME, DIMENSION_UNIQUE_NAME "
        f"FROM $SYSTEM.MDSCHEMA_HIERARCHIES "
        f"WHERE CUBE_NAME='{cube}' AND HIERARCHY_IS_VISIBLE=1 "
        f"ORDER BY DIMENSION_NAME"
    )
    cols, rows = fetch_limited(q, 0)
    seen: set[str] = set()
    dims = []
    for r in rows:
        unique_name = r[1]
        if unique_name not in seen:
            seen.add(unique_name)
            dims.append({"dimension_name": r[0], "dimension_unique_name": unique_name})
    return dims

@router.get("/hierarchies")
def hierarchies(cube: str = Query(...), dimension_unique_name: str | None = None):
    where = f"AND DIMENSION_UNIQUE_NAME='{dimension_unique_name}'" if dimension_unique_name else ""
    q = f"SELECT HIERARCHY_NAME, HIERARCHY_UNIQUE_NAME, DIMENSION_UNIQUE_NAME FROM $SYSTEM.MDSCHEMA_HIERARCHIES WHERE CUBE_NAME='{cube}' AND HIERARCHY_IS_VISIBLE=1 {where} ORDER BY HIERARCHY_NAME"
    cols, rows = fetch_limited(q, 0)
    return [{"hierarchy_name": r[0], "hierarchy_unique_name": r[1], "dimension_unique_name": r[2]} for r in rows]

@router.get("/levels")
def levels(cube: str = Query(...), hierarchy_unique_name: str = Query(...)):
    q = f"SELECT LEVEL_NAME, LEVEL_UNIQUE_NAME, LEVEL_NUMBER FROM $SYSTEM.MDSCHEMA_LEVELS WHERE CUBE_NAME='{cube}' AND HIERARCHY_UNIQUE_NAME='{hierarchy_unique_name}' ORDER BY LEVEL_NUMBER"
    cols, rows = fetch_limited(q, 0)
    return [{"level_name": r[0], "level_unique_name": r[1], "level_number": r[2]} for r in rows]

@router.get("/members")
def members(cube: str = Query(...), level_unique_name: str = Query(...), search: str | None = None, limit: int = 1000):
    like = ""
    if search:
        s = search.replace("'", "''")
        like = f" AND UPPER(MEMBER_CAPTION) LIKE UPPER('%{s}%')"
    q = f"SELECT MEMBER_CAPTION, MEMBER_UNIQUE_NAME FROM $SYSTEM.MDSCHEMA_MEMBERS WHERE CUBE_NAME='{cube}' AND LEVEL_UNIQUE_NAME='{level_unique_name}'{like} ORDER BY MEMBER_CAPTION"
    cols, rows = fetch_limited(q, limit)
    return [{"caption": r[0], "unique_name": r[1]} for r in rows]
