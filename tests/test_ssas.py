from unittest.mock import MagicMock
import types
import sys
import pytest

import backend.app.ssas as ssas


def test_process_cube_missing_pythonnet(monkeypatch):
    monkeypatch.setattr(ssas, "clr", None)
    with pytest.raises(ImportError):
        ssas.process_cube("server", "db")


def test_process_cube_calls_net(monkeypatch):
    fake_server = MagicMock()
    fake_db = fake_server.Databases.__getitem__.return_value

    monkeypatch.setattr(ssas, "clr", object())
    monkeypatch.setattr(ssas, "Assembly", MagicMock(LoadWithPartialName=MagicMock()))
    monkeypatch.setitem(ssas.__dict__, "_import_error", None)

    mod = types.ModuleType("Microsoft.AnalysisServices")
    mod.Server = MagicMock(return_value=fake_server)
    mod.ProcessType = MagicMock(ProcessFull="FULL")
    sys.modules["Microsoft.AnalysisServices"] = mod

    ssas.process_cube("server", "db")

    fake_server.Connect.assert_called_with("server")
    fake_db.Process.assert_called_with(mod.ProcessType.ProcessFull)
