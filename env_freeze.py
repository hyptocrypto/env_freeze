from importlib.util import find_spec
import subprocess
from string import Template
from pathlib import Path
from distutils.sysconfig import get_python_lib

ROOT_DIR = Path(__file__).parent
PYENV = Path(get_python_lib())
PY_BIN = PYENV.parent.parent.parent.joinpath("bin/python")
REQUIRED_PKGS = ["wheel", "setuptools"]


def _run_cmd(cmd: list):
    """Wrapper to run subprocess and hide output"""
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _gen_setup(dir: Path, pkg_name: str) -> None:
    """Generate setup.py in package dir"""
    with open("setup.template", "r") as f:
        data = Template(f.read())
        data = data.substitute(name=pkg_name)
    with open(dir.joinpath("setup.py"), "w+") as f:
        f.write(data)


def _build_wheel(dir: Path, pkg_name: str) -> None:
    """Run shell commands to build wheel and clean up"""
    _gen_setup(dir, pkg_name)
    _run_cmd(["cd", str(dir)])
    _run_cmd([PY_BIN, dir.joinpath("setup.py"), "bdist_wheel"])
    _run_cmd(["cd", ROOT_DIR])
    _run_cmd(["rm", "-rf", ROOT_DIR.joinpath(f"{pkg_name}.egg-info")])
    _run_cmd(["rm", "-rf", ROOT_DIR.joinpath("build")])


def _build_reqs_txt():
    """Create env_freeze_requirements.txt from wheels dir"""
    file_names = [
        str(file).rpartition("/")[-1]
        for file in list(ROOT_DIR.joinpath("dist").iterdir())
        if str(file).endswith(".whl")
    ]
    with open(f"{ROOT_DIR}/env_freeze_requirements.txt", "w+") as f:
        for file in file_names:
            f.write(f"dist/{file}\n")


if __name__ == "__main__":
    # Ensure required packages are installed
    if not all(bool(find_spec(i)) for i in REQUIRED_PKGS):
        raise Exception(f"Env must include following package: {REQUIRED_PKGS}")

    for dir in PYENV.iterdir():
        if not dir.is_dir():
            continue
        if all(not str(p).endswith(".py") for p in list(dir.iterdir())):  # No .py files
            continue
        pkg_name = str(dir).rpartition("/")[-1]
        _build_wheel(dir, pkg_name)

    _build_reqs_txt()
