[% if use_tailwindcss -%]
import os
import subprocess
import sys

from ..main import app


def spawn_child_process(cmd, **kwargs):
    extra = {}
    if sys.platform.startswith("win"):
        extra["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore
    else:
        extra["preexec_fn"] = os.setsid

    kwargs.update(extra)
    return subprocess.Popen(cmd, **kwargs)


class AppCL(app.CL):
    """Custom commands for this application"""
    def run(self):
        spawn_child_process([
            "tailwindcss",
            "-i", "static/css/_input.css",
            "-o", "static/css/styles.css",
            "--watch",
        ])
        super().run()   # type: ignore
[% else %]
from ..main import app


class AppCL(app.CL):
    """Custom commands for this application"""
    pass
[% endif %]
