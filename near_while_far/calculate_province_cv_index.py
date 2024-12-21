import numpy as np
import pandas as pd


def calculate_cv(df, province_col, city_col, year_col, value_col):
    """
    按照省份和年份计算CV值
    :param df: 数据表
    :param province_col: 省份列名称
    :param city_col: 城市列名称
    :param year_col: 年份列名称
    :param value_col: 指标值列名称
    :return: 含有省份、年份和对应CV值的新DataFrame
    """
    # 按照省份和年份分组
    grouped = df.groupby([province_col, year_col])

    # 定义计算CV的函数
    def compute_cv(group):
        x_bar = group[value_col].mean()  # 计算均值
        n = len(group)  # 城市数量
        if n > 1 and x_bar != 0:  # 确保有多个城市且均值不为0
            variance_sum = ((group[value_col] - x_bar) ** 2).sum()  # 计算方差的分子
            cv = np.sqrt(n * variance_sum) / x_bar  # 按公式计算CV
            return cv
        else:
            return np.nan  # 如果只有一个城市或均值为0，返回NaN

    # 应用计算函数并生成结果
    cv_results = grouped.apply(compute_cv).reset_index(name='CV')

    return cv_results

if __name__ == '__main__':
    df = pd.read_excel('/Users/gaoxu/uni/科研/虚拟临近/data/省份_城市_年份_借用规模面板.xlsx')
    result_df = calculate_cv(df, province_col='province', city_col='city', year_col='year', value_col='borrowing_scale')
    result_df.to_excel('result.xlsx')