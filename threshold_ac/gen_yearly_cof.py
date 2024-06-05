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
    df = df.sort_values(by='人口', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    # 应用帕累托回归公式
    df['ln_rank'] = np.log(df['rank'] - 0.5)
    df['ln_size'] = np.log(df['人口'])

    # 进行OLS回归
    X = sm.add_constant(df['ln_size'])
    model = sm.OLS(df['ln_rank'], X)
    results = model.fit()

    # 提取帕累托系数
    return -results.params['ln_size']


if __name__ == '__main__':
    # 加载d第六次全国人口普查数据
    data6 = pd.read_excel('/Users/gaoxu/resources/人口普查数据/第六次全国人口普查.xlsx')
    data7 = pd.read_excel('/Users/gaoxu/resources/人口普查数据/第七次全国人口普查.xlsx')
    print(type(data6))
    # 计算每个省份每年的帕累托系数
    cof6 = calculate_pareto_coefficient(data6)
    cof7 = calculate_pareto_coefficient(data7)
    # 给出结果：
    print('第六次全国人口普查帕累托系数', cof6)
    print('第七次全国人口普查帕累托系数', cof7)

