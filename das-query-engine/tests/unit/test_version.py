import pytest
from utils.version import compare_major_versions, compare_minor_versions, compare_patch_versions

@pytest.mark.parametrize("version1, version2, expected", [
    ("1.2.3", "1.3.0", -1),
    ("2.0.0", "1.3.5", 1),
    ("3.0.0", "3.0.0", 0),
    ("1.2.3", "invalid", None)
])
def test_compare_major_versions(version1, version2, expected):
    assert compare_major_versions(version1, version2) == expected

@pytest.mark.parametrize("version1, version2, expected", [
    ("1.2.3", "1.2.4", 0),
    ("2.0.0", "2.1.5", -1),
    ("3.0.0", "3.0.0", 0),
    ("1.2.3", "invalid", None)
])
def test_compare_minor_versions(version1, version2, expected):
    assert compare_minor_versions(version1, version2) == expected

@pytest.mark.parametrize("version1, version2, expected", [
    ("1.2.3", "1.2.3", 0),
    ("2.0.0", "2.1.5", -1),
    ("3.0.0", "3.0.1", -1),
    ("1.2.3", "invalid", None)
])
def test_compare_patch_versions(version1, version2, expected):
    assert compare_patch_versions(version1, version2) == expected