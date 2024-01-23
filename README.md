# pd_safe_merge
Expands Pandas merge functionality by delivering pre-merge tests and a wrapper function that performs an inner-merge if and only if this both dataframes are a 'perfect match'. 

Two dataframes are a perfect match if:
- Each value in the left dataframe's merge column has at least one matching value in the right dataframe's merge column. 
- Each value in the left dataframe's merge column has at most one matching value in the right dataframe's merge column.

These two conditions are checked by two separate functions so either one can be enforced separately.
