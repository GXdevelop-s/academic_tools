import pandas as pd
import numpy as np
import statsmodels.api as sm

def calculate_pareto_coefficient(df):
    """
    计算帕累托系数、其显著性（p 值）及标准误差
    :param df: DataFrame，包含某个省份某年的所有城市及其人口数据
    :return: 帕累托系数、p 值和标准误差
    """
    # 按人口数量降序排序并计算排名
    df = df.sort_values(by='城市区域人口数量', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    # 应用帕累托回归公式
    df['ln_rank'] = np.log(df['rank'])
    df['ln_size'] = np.log(df['城市区域人口数量'])

    # 进行OLS回归
    X = sm.add_constant(df['ln_size'])
    model = sm.OLS(df['ln_rank'], X)
    results = model.fit()

    # 提取帕累托系数、p 值和标准误差
    pareto_coefficient = -results.params['ln_size']
    p_value = results.pvalues['ln_size']
    se = results.bse['ln_size']

    return pareto_coefficient, p_value, se

if __name__ == '__main__':
    # 加载数据
    data = pd.read_excel('省份_年份_城市_人口_panel_data.xlsx')

    # 计算每年全国的帕累托系数、p 值和标准误差
    results = data.groupby('年份').apply(calculate_pareto_coefficient)

    # 将Series转换为DataFrame
    results_df = results.reset_index()
    results_df.columns = ['Year', 'Pareto_Coefficient_Pvalue_SE']
    results_df[['Pareto_Coefficient', 'P_Value', 'SE']] = pd.DataFrame(results_df['Pareto_Coefficient_Pvalue_SE'].tolist(), index=results_df.index)

    # 将结果保存到新的Excel文件
    results_df.to_excel('pareto_coefficients_pvalues_SE_country_byyear.xlsx', index=False)
