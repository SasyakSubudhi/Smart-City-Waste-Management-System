import zipfile

import pytest

import build_release


def make_project(root, skip=()):
    for name in build_release.APP_FILES + build_release.REPORTS:
        if name not in skip:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)
    package = root / "src" / "waste_mgmt"
    package.mkdir(parents=True)
    for name in ("__init__.py", "bins.py"):
        (package / name).write_text("")


def test_archive_holds_app_package_and_reports(tmp_path):
    make_project(tmp_path)
    output = tmp_path / "release.zip"

    names = build_release.build(output, root=tmp_path)

    with zipfile.ZipFile(output) as archive:
        archived = archive.namelist()
    assert archived == [f"{build_release.PREFIX}/{name}" for name in names]
    assert f"{build_release.PREFIX}/app.py" in archived
    assert f"{build_release.PREFIX}/src/waste_mgmt/bins.py" in archived
    assert f"{build_release.PREFIX}/docs/Unit_Test_Report.md" in archived


def test_missing_report_stops_the_release(tmp_path):
    make_project(tmp_path, skip=("docs/Branch_Coverage_Report.md",))
    output = tmp_path / "release.zip"

    with pytest.raises(FileNotFoundError, match="Branch_Coverage_Report"):
        build_release.build(output, root=tmp_path)
    assert not output.exists()


def test_main_reports_success_and_failure(tmp_path):
    output = str(tmp_path / "out.zip")

    assert build_release.main(["--output", output], root=tmp_path) == 1
    make_project(tmp_path)
    assert build_release.main(["--output", output], root=tmp_path) == 0


def test_real_repository_has_every_release_file():
    names = build_release.release_files()

    assert "src/waste_mgmt/routing.py" in names
    assert len(names) == len(set(names))
