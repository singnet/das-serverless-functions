import pytest
from utils.version import compare_major_versions, compare_minor_versions, compare_patch_versions


@pytest.mark.parametrize(
    "version1, version2, expected",
    [
        ("1.2.3", "1.3.0", 0),
        ("2.0.0", "1.3.5", 1),
        ("2.0.0", "3.0.0", -1),
        ("1.2.3", "invalid", None),
    ],
)
def test_compare_major_versions(version1, version2, expected):
    if version1 == "invalid" or version2 == "invalid":
        with pytest.raises(TypeError):
            compare_major_versions(version1, version2)
    else:
        result = compare_major_versions(version1, version2)
        assert (
            result == expected
        ), f"\nVersion 1: {version1}\nVersion 2: {version2}\nExpected: {expected}\nResult: {result}"


@pytest.mark.parametrize(
    "version1, version2, expected",
    [
        ("1.2.3", "1.2.4", 0),
        ("2.0.0", "2.1.5", -1),
        ("3.0.0", "3.0.0", 0),
        ("1.2.3", "invalid", None),
    ],
)
def test_compare_minor_versions(version1, version2, expected):
    if version1 == "invalid" or version2 == "invalid":
        with pytest.raises(TypeError):
            compare_minor_versions(version1, version2)
    else:
        result = compare_minor_versions(version1, version2)
        assert (
            result == expected
        ), f"\nVersion 1: {version1}\nVersion 2: {version2}\nExpected: {expected}\nResult: {result}"


@pytest.mark.parametrize(
    "version1, version2, expected",
    [
        ("1.2.3", "1.2.3", 0),
        ("2.0.0", "2.1.5", -1),
        ("3.0.0", "3.0.1", -1),
        ("1.2.3", "invalid", None),
    ],
)
def test_compare_patch_versions(version1, version2, expected):
    if version1 == "invalid" or version2 == "invalid":
        with pytest.raises(TypeError):
            compare_patch_versions(version1, version2)
    else:
        result = compare_patch_versions(version1, version2)
        assert (
            result == expected
        ), f"\nVersion 1: {version1}\nVersion 2: {version2}\nExpected: {expected}\nResult: {result}"
