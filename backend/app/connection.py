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

_conn = None


def open_connection():
    """Return a singleton Pyadomd connection using the configured settings."""
    global _conn

    if Pyadomd is None or clr is None:
        raise RuntimeError("pyadomd library not installed")

    if _conn is not None:
        return _conn

    if settings.adomd_dll_path:
        os.add_dll_directory(os.path.dirname(settings.adomd_dll_path))
        Assembly.LoadFrom(settings.adomd_dll_path)

    _conn = Pyadomd(get_conn_str())
    _conn.open()
    return _conn


def close_connection() -> None:
    """Close the global cube connection, if open."""
    global _conn
    if _conn is not None:
        try:
            _conn.close()
        finally:
            _conn = None
