import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')  # 支持中文的字体路径

# 从Excel文件中加载数据
file_path = '/Users/gaoxu/uni/科研/cityranksize/中文版本/数据/pareto_coefficients_at_least_14_2011_2021.xlsx'
data_2011 = pd.read_excel(file_path, sheet_name='2011')
data_2021 = pd.read_excel(file_path, sheet_name='2021')

# 省份数量
categories = np.arange(len(data_2011['省份'].unique()))  # 使用数字标签代替省份名称

# 标签位置
x = np.arange(len(categories))

width = 0.35  # 条形的宽度

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, data_2011['帕累托系数'], width, label='2011', color='white', edgecolor='black',
                linewidth=2)
rects2 = ax.bar(x + width / 2, data_2021['帕累托系数'], width, label='2021', color='grey', edgecolor='black')

# 添加一些文本标签，标题以及自定义x轴刻度标签等
ax.set_xlabel('省份编号', fontproperties=font)
ax.set_ylabel('帕累托系数', fontproperties=font)
ax.set_title('2011、2021各省帕累托系数', fontproperties=font)
ax.set_xticks(x)
ax.set_xticklabels(categories + 1, fontproperties=font)  # 使用1开始的编号代替省份名称
ax.legend()

fig.tight_layout()
plt.savefig('/Users/gaoxu/Desktop/pareto_coefficients_plot.jpg',dpi=300)  # 指定文件名并保存到桌面
plt.show()
