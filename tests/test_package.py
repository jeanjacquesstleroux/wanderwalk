"""Packaging contract: the public API, version, and optional app extra."""

import importlib
import re

import pytest

import wanderwalk

EXPECTED_API = {
    "Manifold",
    "PoincareDisk",
    "Sphere",
    "Torus",
    "boundary_angle_histogram",
    "disk_kde",
    "hyperbolic_simulator",
    "sphere_kde",
    "sphere_simulator",
    "torus_simulator",
    "__version__",
}


class TestPublicApi:
    def test_all_matches_the_documented_api(self):
        assert set(wanderwalk.__all__) == EXPECTED_API

    @pytest.mark.parametrize("name", sorted(EXPECTED_API))
    def test_every_exported_name_is_reachable(self, name):
        assert getattr(wanderwalk, name) is not None

    def test_version_is_pep440_compatible(self):
        assert re.fullmatch(r"\d+\.\d+\.\d+([a-z]+\d+)?", wanderwalk.__version__)

    @pytest.mark.parametrize(
        "module",
        [
            "wanderwalk.manifolds",
            "wanderwalk.simulation",
            "wanderwalk.visualization",
        ],
    )
    def test_subpackages_import_and_declare_exports(self, module):
        assert importlib.import_module(module).__all__

    def test_installed_metadata_matches_dunder_version(self):
        # Skipped for a bare source checkout, where the dist is not installed
        metadata = pytest.importorskip("importlib.metadata")
        try:
            installed = metadata.version("wanderwalk")
        except metadata.PackageNotFoundError:
            pytest.skip("wanderwalk is not installed as a distribution")
        assert installed == wanderwalk.__version__

    def test_core_import_does_not_pull_in_app_dependencies(self):
        # The core install is numpy-only, so importing the library must not
        # require streamlit or plotly
        import sys

        for heavy in ("streamlit", "plotly"):
            sys.modules.pop(heavy, None)
        importlib.reload(wanderwalk)
        assert "streamlit" not in sys.modules
        assert "plotly" not in sys.modules


class TestAppLauncher:
    def test_launcher_imports_without_streamlit_installed(self):
        from wanderwalk.app import cli

        assert callable(cli.main)

    def test_app_path_points_at_the_bundled_app(self):
        from wanderwalk.app import cli

        assert cli.APP_PATH.name == "streamlit_app.py"
        assert cli.APP_PATH.is_file()

    def test_missing_deps_reports_a_list(self):
        from wanderwalk.app import cli

        assert isinstance(cli._missing_deps(), list)

    def test_main_explains_how_to_install_the_extra(self, monkeypatch):
        from wanderwalk.app import cli

        monkeypatch.setattr(cli, "_missing_deps", lambda: ["streamlit"])
        with pytest.raises(SystemExit, match=r"wanderwalk\[app\]"):
            cli.main([])
