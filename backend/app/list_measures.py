import os
from .connection import open_connection

SQL = """
SELECT
    MEASURE_NAME
FROM
    $SYSTEM.MDSCHEMA_MEASURES
WHERE
    CUBE_NAME = '{cube}'
ORDER BY
    MEASURE_NAME
"""


def main() -> None:
    cube = os.environ.get("CUBE_NAME", "")
    if not cube:
        raise SystemExit("CUBE_NAME environment variable not set")

    sql = SQL.format(cube=cube)
    conn = open_connection()
    with conn.cursor() as cur:
        cur.execute(sql)
        measures = [row[0] for row in cur.fetchall()]

    for m in measures:
        print(m)


if __name__ == "__main__":
    main()
