"""Package the dashboard, the domain package and the validation reports.

The Release workflow runs this after CI passes on main. The archive holds
everything needed to run the dashboard plus the four reports generated for
the same commit. Run locally with: python build_release.py
"""

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "smart-city-waste-management"
APP_FILES = ["app.py", "demo.py", "requirements.txt", "README.md", "LICENSE"]
REPORTS = [
    "docs/Unit_Test_Report.md",
    "docs/System_Validation_Report.md",
    "docs/Code_Coverage_Report.md",
    "docs/Branch_Coverage_Report.md",
]


def release_files(root=ROOT):
    """Return the archive's files as forward-slash paths relative to root.

    Raises FileNotFoundError naming every required file that is missing, so a
    release is never published without its reports or package.
    """
    root = Path(root)
    package = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "src" / "waste_mgmt").glob("*.py")
    )
    missing = [name for name in APP_FILES + REPORTS if not (root / name).is_file()]
    if not package:
        missing.append("src/waste_mgmt/*.py")
    if missing:
        raise FileNotFoundError("Missing release files: " + ", ".join(missing))
    return APP_FILES + package + REPORTS


def build(output, root=ROOT):
    """Write the release archive to output and return the archived names."""
    root = Path(root)
    names = release_files(root)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(root / name, f"{PREFIX}/{name}")
    return names


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", default=f"{PREFIX}.zip")
    args = parser.parse_args(argv)
    try:
        names = build(args.output, root)
    except FileNotFoundError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote {args.output} with {len(names)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
