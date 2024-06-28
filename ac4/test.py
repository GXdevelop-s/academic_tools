import os
import time

import numpy as np
import pandas as pd

if __name__ == '__main__':
    start = time.time()
    directory_path = r'/Users/gaoxu/uni/科研/工商业全量/数据/全国数据'
    all_files = os.listdir(directory_path)
    # 最终的分类信息
    all_category = pd.Series()
    # 开始循环处理目录中的文件
    for file in all_files:
        if file.endswith('.xlsx'):
            # 文件绝对路径
            file_path = os.path.join(directory_path, file)
            print(file_path)
            data = pd.read_excel(file_path)
            curr_category = data['企业类型']
            combined_series = pd.concat([all_category, curr_category], ignore_index=True)
            all_category = combined_series
        else:
            continue
    # 去除 NaN 值
    all_category = all_category.dropna()
    # 筛选包含 '农' 字的分类
    filtered_category = all_category[all_category.str.contains('农')]
    # 计数
    category_info = filtered_category.value_counts()
    # 将 Series 转换为 DataFrame
    counts_df = category_info.to_frame()
    # 转置 DataFrame
    transposed_df = counts_df.T
    print(transposed_df)
    transposed_df.to_excel('企业分类数量all.xlsx')
    end = time.time()
    print(f'所用时间为{end - start}seconds')
