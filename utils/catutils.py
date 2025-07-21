import pandas as pd
import re
from typing import Mapping, Iterable, Dict


def categorize_in_place(
        df: pd.DataFrame,
        category_patterns: Mapping[str, re.Pattern],
        add_no_category: bool =  True,
        name_cln: str = 'name',
) -> None:
    """
    Add boolean category columns to a DataFrame based on regex patterns.

    Each pattern is matched against the values in `name_cln` column.
    Adds a 'no_cat' column for rows not matching any pattern (if `add_no_category=True`).

    Modifies the DataFrame in-place.
    """
    for category, pattern in category_patterns.items():
        df[category] = df[name_cln].str.contains(pattern)

    categories = list(category_patterns.keys())
    mask_all_cat = df[categories].any(axis=1)
    if add_no_category:
        df["no_cat"] = ~mask_all_cat

def category_count(df: pd.DataFrame, categories: Iterable[str]) -> Dict[str, int]:
    return {cat: int(df[cat].sum()) for cat in categories}