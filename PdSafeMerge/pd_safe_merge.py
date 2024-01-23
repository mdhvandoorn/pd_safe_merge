import pandas as pd


class ImperfectMergeError(Exception):
    """Raised when some condition is not met regarding the values in the left 
    dataframe's merge column w.r.t. the values in the right dataframe's merge 
    column."""


def check_left_all_matched(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_on: str,
    right_on: str,
) -> None:
    """Check if each value in the left dataframe's merge column has at least one 
    matching value in the right dataframe's merge column, and raise an 
    ImperfectMergeError otherwise.

    Args:
        df_left (pd.DataFrame): 
            The left dataframe.
        df_right (pd.DataFrame): 
            The right dataframe.
        left_on (str): 
            The column name of the left dataframe's merge column.
        right_on (str): 
            The column name of the right dataframe's merge column.

    Raises:
        ImperfectMergeError
            Error that indicates that the aforementioned condition was not 
            satisfied.
    """
    df_merged = df_left.merge(
        df_right, how="left", indicator=True, left_on=left_on, right_on=right_on
    )
    df_non_matched = df_merged.loc[df_merged["_merge"] == "left_only"]

    if df_non_matched.shape[0] > 0:
        raise ImperfectMergeError(
            "df_left's merge column has values that are not in df_right's merge column"
        )


def check_left_duplicate_matches(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_on: str,
    right_on: str,
) -> None:
    """Check if each value in the left dataframe's merge column has at most one
    matching value in the right dataframe's merge column, and raise an 
    ImperfectMergeError otherwise.

    Args:
        df_left (pd.DataFrame): 
            The left dataframe.
        df_right (pd.DataFrame): 
            The right dataframe.
        left_on (str): 
            The column name of the left dataframe's merge column.
        right_on (str): 
            The column name of the right dataframe's merge column.

    Raises:
        ImperfectMergeError
            Error that indicates that the aforementioned condition was not 
            satisfied.
    """
    left_merge_values = df_left[left_on].tolist()
    right_duplicates = df_right[df_right.duplicated(right_on)][right_on].tolist()

    if any(item in right_duplicates for item in left_merge_values):
        raise ImperfectMergeError(
            (
                "df_right's merge column contains duplicate matches to the values"
                " in df_left's merge column"
            )
        )


def check_perfect_match(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_on: str,
    right_on: str,
) -> None:
    """Check if each value in the left dataframe's merge column has a unique 
    match in the right dataframe's merge column.

    Separately check two conditions:
    - Each value in the left dataframe's merge column should have at least one
    matching value in the right dataframe's merge column. 
    - Each value in the left dataframe's merge column should have at most one
    matching value in the right dataframe's merge column. 

    Args:
        df_left (pd.DataFrame): 
            The left dataframe.
        df_right (pd.DataFrame): 
            The right dataframe.
        left_on (str): 
            The column name of the left dataframe's merge column.
        right_on (str): 
            The column name of the right dataframe's merge column.

    Raises:
        ImperfectMergeError: 
            Error that indicates that the aforementioned conditions were not 
            satisfied. Aggregate the errors of the individual merge check 
            functions and re-raise them.
             
    """
    errors = []
    try:
        check_left_all_matched(df_left, df_right, left_on, right_on)
    except ImperfectMergeError as e:
        errors.append(e)

    try:
        check_left_duplicate_matches(df_left, df_right, left_on, right_on)
    except ImperfectMergeError as e:
        errors.append(e)

    if errors:
        raise ImperfectMergeError("; ".join(str(error) for error in errors))


def safe_inner_merge(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_on: str,
    right_on: str,
) -> pd.DataFrame:
    """Check if each value in the left dataframe's merge column has a unique 
    match in the right dataframe's merge column and return the inner-merged 
    result if this is the case.

    Args:
        df_left (pd.DataFrame): 
            The left dataframe.
        df_right (pd.DataFrame): 
            The right dataframe.
        left_on (str): 
            The column name of the left dataframe's merge column.
        right_on (str): 
            The column name of the right dataframe's merge column.

    Returns:
        pd.DataFrame: 
            The inner-merged dataframe.
    """
    check_perfect_match(
        df_left=df_left, df_right=df_right, left_on=left_on, right_on=right_on
    )

    df_merged = df_left.merge(right=df_right, left_on=left_on, right_on=right_on)

    return df_merged
