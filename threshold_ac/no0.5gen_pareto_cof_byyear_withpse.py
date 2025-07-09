import pandas as pd
import numpy as np
import statsmodels.api as sm


def calculate_pareto_coefficient(df):
    """
    to calculate pareto coefficient,p_value and stand error
    :param df: DataFrame，Include all cities in a certain province and their population data for a specific year.
    :return: pareto coefficient,p_value and stand error
    """
    # rank by population
    df = df.sort_values(by='urban_scale', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    # Applying the Pareto regression formula
    df['ln_rank'] = np.log(
        df['rank'])  # The improved formula (Eq. 3 in text) simply changes df['rank'] to df['rank']-0.5
    df['ln_size'] = np.log(df['urban_scale'])

    # OLS regression
    X = sm.add_constant(df['ln_size'])
    model = sm.OLS(df['ln_rank'], X)
    results = model.fit()

    # extract pareto coefficient p_value and stand error
    pareto_coefficient = -results.params['ln_size']
    p_value = results.pvalues['ln_size']
    se = results.bse['ln_size']

    return pareto_coefficient, p_value, se


if __name__ == '__main__':
    # load data
    data = pd.read_excel('province_year_city_population_panel_data.xlsx')

    # calculate pareto coefficient,p_value and stand error in every year
    results = data.groupby('year').apply(calculate_pareto_coefficient)

    # turn Series to DataFrame
    results_df = results.reset_index()
    results_df.columns = ['Year', 'Pareto_Coefficient_Pvalue_SE']
    results_df[['Pareto_Coefficient', 'P_Value', 'SE']] = pd.DataFrame(
        results_df['Pareto_Coefficient_Pvalue_SE'].tolist(), index=results_df.index)

    # save to a new Excel file
    results_df.to_excel('pareto_coefficients_pvalues_SE_country_byyear.xlsx', index=False)
