import os
from .config import settings

try:
    import clr  # type: ignore
    from System.Reflection import Assembly  # type: ignore
    from pyadomd import Pyadomd  # type: ignore
except Exception:  # pragma: no cover - import errors
    clr = None
    Assembly = None
    Pyadomd = None

# Default connection string matching the example
CONN_STR = (
    "Provider=MSOLAP;"
    "Data Source=server;"
    "Initial Catalog=Cube8;"
    "Integrated Security=SSPI;"
)

def get_conn_str() -> str:
    """Return configured connection string or the default example."""
    return settings.adomd_conn_str or CONN_STR

def open_connection():
    """Return a Pyadomd connection object using the configured settings."""
    if Pyadomd is None or clr is None:
        raise RuntimeError("pyadomd library not installed")
    if settings.adomd_dll_path:
        os.add_dll_directory(os.path.dirname(settings.adomd_dll_path))
        Assembly.LoadFrom(settings.adomd_dll_path)
    return Pyadomd(get_conn_str())
