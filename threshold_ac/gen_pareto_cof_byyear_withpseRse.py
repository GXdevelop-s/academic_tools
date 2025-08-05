import pandas as pd
import numpy as np
import statsmodels.api as sm


def pareto_with_se(df, cov_type: str = "HC0", cluster_col: str | None = None) -> pd.Series:
    """
    Compute the Pareto coefficient and return both OLS and robust
    (heteroskedastic- or cluster-robust) standard errors and p-values.

    Parameters
    ----------
    df : pandas.DataFrame
        Data for a single year (or province–year) containing all cities and
        the column ``'urban_scale'`` with population size.
    cov_type : {"HC0", "HC1", "HC2", "HC3", "cluster"}, default "HC0"
        Type of robust covariance estimator.
        * "HC0"–"HC3"  → White heteroskedasticity-robust SEs.
        * "cluster"    → Cluster-robust SEs; requires ``cluster_col``.
    cluster_col : str or None
        Column used to define clusters when ``cov_type="cluster"``
        (e.g., ``'province'`` or ``'city_id'``).

    Returns
    -------
    pandas.Series
        Series with the Pareto coefficient and two sets of SEs and p-values:
        - ``'SE_OLS'`` / ``'P_Value_OLS'``    : conventional OLS
        - ``'SE_Robust'`` / ``'P_Value_Robust'`` : robust (HC or cluster)
    """
    # 1. Rank cities by population size (descending)
    df = df.sort_values('urban_scale', ascending=False).copy()
    df['rank'] = np.arange(1, len(df) + 1)

    # 2. # Applying the Pareto regression formula
    df['ln_rank'] = np.log(
        df['rank'] )   # The improved formula (Eq. 3 in text) simply changes df['rank'] to df['rank']-0.5
    df['ln_size'] = np.log(df['urban_scale'])

    # 3. OLS regression ln(rank) = α + β·ln(size)
    X = sm.add_constant(df['ln_size'])
    ols_res = sm.OLS(df['ln_rank'], X).fit()

    # 4. Robust covariance estimator
    if cov_type == "cluster" and cluster_col:
        rob_res = ols_res.get_robustcov_results(
            cov_type="cluster",
            groups=df[cluster_col]
        )
    else:                                      # HC0/HC1/HC2/HC3
        rob_res = ols_res.get_robustcov_results(cov_type=cov_type)

    # 5. Extract coefficient and both sets of SEs / p-values
    coef   = -ols_res.params['ln_size']                                   # Pareto coefficient (note the minus sign)
    se_ols =  ols_res.bse['ln_size']
    p_ols  =  ols_res.pvalues['ln_size']

    # Convert ndarray to Series with parameter names for easy access
    se_rob = pd.Series(rob_res.bse,     index=rob_res.model.exog_names)['ln_size']
    p_rob  = pd.Series(rob_res.pvalues, index=rob_res.model.exog_names)['ln_size']

    return pd.Series({
        'Pareto_Coefficient': coef,
        'SE_OLS':            se_ols,
        'P_Value_OLS':       p_ols,
        'SE_Robust':         se_rob,
        'P_Value_Robust':    p_rob,
    })


if __name__ == '__main__':
    # Load the panel data (province–year–city population)
    data = pd.read_excel('省份_年份_城市_人口_panel_data_2011_2021.xlsx')

    # ===== Example 1: yearly results with White HC0 robust SEs =====
    yearly_out = (
        data.groupby('year')
            .apply(pareto_with_se, cov_type="HC0")
            .reset_index()
            .rename(columns={'year': 'Year'})
    )
    yearly_out.to_excel('test.xlsx', index=False)
