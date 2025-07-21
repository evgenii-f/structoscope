import re
from typing import List


def remove_last_n_parts(path: str, n: int = 2) -> str:
    """
    Remove the last `n` parts from a slash-separated path string.

    Example:
        >>> remove_last_n_parts("a/b/c/d", 2)
        'a/b'
    """
    return "/".join(path.split("/")[:-n])


def strip_path_until(path: str, anchors: List[str]) -> str:
    """
    Strip everything from the left of the first occurrence of an anchor (inclusive).
    Uses regex pattern matching.

    Example:
        >>> strip_path_until("home/user/data/VASP_test/abc", ["VASP_test"])
        '/abc'

    Warning:
        If anchor occurs in filename (not path), it may cut unexpectedly.
    """
    pattern = rf'.*?({"|".join(anchors)})'
    return re.sub(pattern, "", path)


def clean_path(path: str, stopwords: List[str], n_strip_right: int = 1) -> str:
    """
    Clean a path by removing its last `n_strip_right` components and stripping everything
    before the first occurrence of any stopword.

    Example:
        >>> clean_path("home/user/VASP_test/foo/bar.xyz", ["VASP_test"], 1)
        '/foo'
    """
    return strip_path_until(remove_last_n_parts(path, n_strip_right), stopwords)
