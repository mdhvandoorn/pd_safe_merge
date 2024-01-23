from pathlib import Path
import sys
import os

import pandas as pd
import pytest

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
sys.path.append(PROJECT_ROOT)

import PdSafeMerge.pd_safe_merge as pd_sm

df_1 = pd.DataFrame({"A": [1, 2, 3], "C": [5, 6, 7]})

df_1_1 = pd.DataFrame({"A": [1, 2], "B": [7, 8]})
df_1_2 = pd.DataFrame({"A": [1, 2, 2], "B": [7, 8, 9]})
df_1_3 = pd.DataFrame({"A": [], "B": []})
df_1_4 = pd.DataFrame({"A": [1, 2, 3], "B": [7, 8, 9]})


@pytest.mark.parametrize(
    "df_left, df_right, left_on, right_on, expect_error",
    [
        (df_1, df_1_1, "A", "A", True),
        (df_1, df_1_2, "A", "A", True),
        (df_1, df_1_3, "A", "A", True),
        (df_1, df_1_4, "A", "A", False),
    ],
)
def test_check_perfect_match(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_on: str,
    right_on: str,
    expect_error: bool,
) -> None:
    if expect_error:
        with pytest.raises(pd_sm.ImperfectMergeError):
            pd_sm.check_perfect_match(
                df_left=df_left, df_right=df_right, left_on=left_on, right_on=right_on
            )
    else:
        pd_sm.check_perfect_match(
            df_left=df_left, df_right=df_right, left_on=left_on, right_on=right_on
        )