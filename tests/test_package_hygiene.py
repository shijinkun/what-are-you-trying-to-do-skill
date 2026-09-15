from pathlib import Path


PACKAGE = Path(__file__).parents[1]


def test_release_package_has_publish_metadata_and_no_runtime_secrets():
    assert (PACKAGE / "README.md").is_file()
    assert (PACKAGE / ".gitignore").is_file()
    assert (PACKAGE / "LICENSE").is_file()

    forbidden_names = {".env", "langsmith.db", "run.log"}
    found = {path.name for path in PACKAGE.rglob("*") if path.is_file()}
    assert not found & forbidden_names
