import pandas as pd
import numpy as np
import statsmodels.api as sm

def calculate_pareto_coefficient(df):
    """
    计算帕累托系数
    :param df: DataFrame，包含某个省份某年的所有城市及其人口数据
    :return: 帕累托系数
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

    # 提取帕累托系数
    return -results.params['ln_size']

if __name__ == '__main__':
    # 加载数据
    data = pd.read_excel('省份_年份_城市_人口_panel_data.xlsx')

    # 计算每年全国的帕累托系数
    pareto_coefficients = data.groupby('年份').apply(calculate_pareto_coefficient)

    # 将Series转换为DataFrame
    pareto_coefficients_df = pareto_coefficients.reset_index()
    pareto_coefficients_df.columns = ['Year', 'Pareto_Coefficient']

    # 将结果保存到新的Excel文件
    pareto_coefficients_df.to_excel('no0.5pareto_coefficients_country_byyear.xlsx', index=False)
