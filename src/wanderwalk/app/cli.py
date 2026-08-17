"""Launcher for the wanderwalk Streamlit app."""

import importlib.util
import sys
from pathlib import Path

APP_PATH = Path(__file__).resolve().parent / "streamlit_app.py"

_OPTIONAL_DEPS = ("streamlit", "plotly")


def _missing_deps():
    """Returns the app's optional dependencies that are not installed."""
    return [
        name
        for name in _OPTIONAL_DEPS
        if importlib.util.find_spec(name) is None
    ]


def main(argv=None):
    """Runs the Streamlit app. Entry point for the wanderwalk-app script.

    Arguments:
        argv: Extra arguments forwarded to "streamlit run". Defaults to the
            arguments this script was called with.

    Returns:
        The exit status from Streamlit.

    Raises:
        SystemExit: If the optional app dependencies are not installed.
    """
    missing = _missing_deps()
    if missing:
        raise SystemExit(
            f"wanderwalk-app needs {' and '.join(missing)}, which the core "
            "install does not include.\n"
            "Install the app extra with:\n\n    pip install wanderwalk[app]"
        )

    from streamlit.web import cli as streamlit_cli

    if argv is None:
        argv = sys.argv[1:]

    # Streamlit's CLI reads sys.argv, so rewrite it before handing off
    sys.argv = ["streamlit", "run", str(APP_PATH), *argv]
    return streamlit_cli.main()


if __name__ == "__main__":
    main()
