import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')  # 支持中文的字体路径
# data 格式: 省份|城市 | 年份 | 规模
data = pd.read_excel('./output_11131821.xlsx')
# 计算增长率
data['growth_rate'] = data.groupby('city_name')['城市区域人口数量'].pct_change()

# 剔除异常值
data = data[(data['growth_rate'] <= 1.01) & (data['growth_rate'] >= -0.95) & (data['growth_rate'] <= 2)]

# 获取城市ID，规模和增长率
sizes = data['城市区域人口数量'].values
growth_rates = data['growth_rate'].values


# 选择指数核函数和带宽
def exponential_kernel(x, h):
    return (1 / h) * np.exp(-np.abs(x) / h)


# 确定带宽 h
h = 0.9 * min(np.std(sizes), np.subtract(*np.percentile(sizes, [75, 25])) / 1.34) * len(sizes) ** (-1 / 5)


# 估计条件均值和方差
def conditional_mean(S, sizes, growth_rates, h):
    weights = exponential_kernel(S - sizes, h)
    return np.sum(weights * growth_rates) / np.sum(weights)


def conditional_variance(S, sizes, growth_rates, h):
    mu_S = conditional_mean(S, sizes, growth_rates, h)
    weights = exponential_kernel(S - sizes, h)
    return np.sum(weights * (growth_rates - mu_S) ** 2) / np.sum(weights)


# 计算每个城市规模的条件均值和方差
# 这里我们将城市规模分为若干个区间来计算
size_grid = np.linspace(min(sizes), max(sizes), 100)
mu_S_estimates = [conditional_mean(S, sizes, growth_rates, h) for S in size_grid]
sigma2_S_estimates = [conditional_variance(S, sizes, growth_rates, h) for S in size_grid]

# 绘制人口规模与增长率均值的图
plt.figure(figsize=(10, 6))
plt.plot(size_grid, mu_S_estimates, label='增长率均值', c='grey')
plt.xlabel('城市规模(标准化的人口)', fontproperties=font)
plt.ylabel('增长率均值', fontproperties=font)
plt.title('城市规模与增长率均值', fontproperties=font)
plt.legend(prop=font)
plt.savefig('/Users/gaoxu/Desktop/growth_rates.jpg', dpi=400)
plt.show()
# 绘制人口规模与方差的图
plt.figure(figsize=(10, 6))
plt.plot(size_grid, sigma2_S_estimates, label='方差', c='grey')
plt.xlabel('城市规模(标准化的人口)', fontproperties=font)
plt.ylabel('方差', fontproperties=font)
plt.title('城市规模与方差', fontproperties=font)
plt.legend(prop=font)
plt.savefig('/Users/gaoxu/Desktop/sigma_rates.jpg', dpi=400)
plt.show()
