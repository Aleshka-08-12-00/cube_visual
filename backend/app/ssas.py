import typing

try:
    import clr  # type: ignore
    from System.Reflection import Assembly
except Exception as e:  # pragma: no cover - import-time errors
    clr = None
    Assembly = None
    _import_error = e
else:
    _import_error = None


def process_cube(server_name: str, db_name: str) -> None:
    """Process an SSAS cube using .NET APIs via pythonnet."""
    if clr is None:
        raise ImportError(f"pythonnet not available: {_import_error}")

    try:
        Assembly.LoadWithPartialName("AnalysisServices.DLL")
    except Exception as e:
        raise RuntimeError(f"Failed to load AnalysisServices.DLL: {e}")

    from Microsoft.AnalysisServices import Server, ProcessType  # type: ignore

    server = Server()
    server.Connect(server_name)

    db = server.Databases[db_name]
    db.Process(ProcessType.ProcessFull)
