import os
import clr
from System.Reflection import Assembly
from pyadomd import Pyadomd

# Path to ADOMD.NET DLL
DLL_PATH = r"C:\Program Files\Microsoft.NET\ADOMD.NET\110\Microsoft.AnalysisServices.AdomdClient.dll"

# Add folder to DLL search path and load the assembly
os.add_dll_directory(os.path.dirname(DLL_PATH))
Assembly.LoadFrom(DLL_PATH)

# Connection string for the cube
CONN_STR = (
    "Provider=MSOLAP;"
    "Data Source=server;"
    "Initial Catalog=Cube8;"
    "Integrated Security=SSPI;"
)

SQL = """
SELECT
    MEASURE_NAME
FROM
    $SYSTEM.MDSCHEMA_MEASURES
WHERE
    CUBE_NAME = 'NextGen'
ORDER BY
    MEASURE_NAME
"""

# Execute a query using pyadomd
with Pyadomd(CONN_STR) as conn:
    with conn.cursor() as cur:
        cur.execute(SQL)
        print([row[0] for row in cur.fetchall()])
