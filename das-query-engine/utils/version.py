import re
from typing import Tuple, Union


def get_version_components(version_string: str) -> Union[Tuple[int], None]:
    pattern = r'^(\d+)\.(\d+)\.(\d+)$'

    match = re.match(pattern, version_string)

    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        return major, minor, patch
    else:
        return None


def compare_major_versions(version1, version2):
    major1, _, _ = get_version_components(version1)
    major2, _, _ = get_version_components(version2)

    if major1 is None or major2 is None:
        return None

    return (major1 > major2) - (major1 < major2)


def compare_minor_versions(version1, version2):
    _, minor1, _ = get_version_components(version1)
    _, minor2, _ = get_version_components(version2)

    if minor1 is None or minor2 is None:
        return None

    return (minor1 > minor2) - (minor1 < minor2)


def compare_patch_versions(version1, version2):
    _, _, patch1 = get_version_components(version1)
    _, _, patch2 = get_version_components(version2)

    if patch1 is None or patch2 is None:
        return None

    return (patch1 > patch2) - (patch1 < patch2)
