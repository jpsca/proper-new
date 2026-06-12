import argparse
import os
import subprocess
import sys
from pathlib import Path

import inflection
from hecto import (
    COLORS,
    confirm,
    printf,
    render_blueprint,
)


APP_BLUEPRINT_REPO = "https://github.com/jpsca/proper.git"


def get_default_blueprint() -> str:
    """Returns the blueprint URL pinned to the latest tag of the repo,
    or pointing at the default branch if the tags cannot be listed.
    """
    tag = get_latest_tag(APP_BLUEPRINT_REPO)
    ref = f"@{tag}" if tag else ""
    return f"{APP_BLUEPRINT_REPO}{ref}#blueprint"


def get_latest_tag(repo_url: str) -> str:
    try:
        out = subprocess.run(
            ["git", "ls-remote", "--tags", "--sort=-v:refname", repo_url],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return ""
    for line in out.splitlines():
        ref = line.rpartition("\t")[2]
        if ref.endswith("^{}"):
            continue
        return ref.removeprefix("refs/tags/")
    return ""


def call(cmd: str) -> None:
    printf("run", cmd, color=COLORS.OK)
    os.system(cmd)


def gen_app(
    path: str | Path,
    *,
    name: str = "",
    src: str = "",
    force: bool = False,
    tailwind: bool = False,
    install_deps: bool = True,
) -> None:
    """Creates a new Proper application at `path`.

    Args:
        path:
            Where to create the new application.
        name:
            Optional name of the app instead of the one in `path`
        force:
            Overwrite files that already exist, without asking.
        install_deps:
            Whether to install dependencies after generating the app.

    """
    path = Path(path).resolve().absolute()
    if path.exists():
        if not force and not confirm("Path already exists. Continue?", default=False):
            return
    else:
        path.mkdir(parents=True, exist_ok=False)

    app_name = inflection.underscore(name.strip() or str(path.stem))

    src = src.strip()
    if src:
        print("Using custom blueprint:", src)
    else:
        src = get_default_blueprint()
        print("Using default blueprint:", src)

    render_blueprint(
        src,
        path,
        context={
            "app_name": app_name,
            "tailwind": tailwind,
        },
        force=force,
    )
    print()

    if not tailwind:
        (path / "static" / "css" / "_tw.css").unlink(missing_ok=True)

    if install_deps:
        _install_dependencies(path)
    wrap_up(path)


def _install_dependencies(path: Path) -> None:
    os.chdir(path)
    venv_path = str(path / ".venv")
    os.environ["VIRTUAL_ENV"] = venv_path
    call(f"""cd {str(path)} \\
            && uv venv \\
            && uv sync --group dev
    """)


def wrap_up(path: Path) -> None:
    print("✨ Done! ✨")
    print()
    print(" The following steps are missing:")
    print()
    print("   $ cd " + path.stem + "")
    print("   $ source .venv/bin/activate")
    print()
    print(" Start your Proper app with:")
    print()
    print("   $ proper run")
    print()


def run():
    usage = "uvx proper_new <path> [--name <app_name>] [--force] [--tailwind]"
    description="""
    The `proper_new` command creates a new Proper application at the path you specify.
    """.strip()

    if len(sys.argv) == 1:
        print("Usage:")
        print(f"    {usage}")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        usage=usage,
        description=description
    )
    parser.add_argument("path", help="The required path argument")
    parser.add_argument("--name", help="Optional name of the app instead of the one in `path`", default="")
    parser.add_argument("--src", help="Optional source url/path of the blueprint instead of the default one", default="")
    parser.add_argument("--force", help="Overwrite files that already exist, without asking", action="store_true")
    parser.add_argument("--tailwind", help="Use Tailwind CSS", action="store_true")
    args = parser.parse_args()
    gen_app(
        args.path,
        name=args.name,
        src=args.src,
        force=args.force,
        tailwind=args.tailwind
    )


def print_banner():
    print("""
░███████████
 ░███    ░███
 ░███    ░███░████████ ░██████ ░████████    ░██████ ░████████
 ░██████████  ░███ ░██░███ ░███ ░███  ░███ ░███ ░███ ░███ ░██
 ░███         ░███    ░███ ░███ ░███  ░███ ░███████  ░███
 ░███         ░███    ░███ ░███ ░███  ░███ ░███      ░███
░█████       ░█████    ░██████  ░███████    ░██████ ░█████
                                ░███
                                ░███
                               ░█████
""")


if __name__ == "__main__":
    print_banner()
    run()
