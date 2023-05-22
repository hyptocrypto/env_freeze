from pathlib import Path


def identify_packages(dir: Path):
    """Iterate over dir and find all possible python package"""

    pkg_names = []
    for dir in list(dir.iterdir()):
        if not dir.is_dir():
            continue
        if not "__init__.py" in str(dir):
            continue
        pkg_names.append(dir)

    return set(pkg_names)
