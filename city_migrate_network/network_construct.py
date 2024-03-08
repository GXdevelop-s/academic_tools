import math

import pandas as pd


def network_construct(year, trimmed_index_df, in_out_df):
    # 初始化城市迁移矩阵
    cities = trimmed_index_df['城市'].tolist()
    now_network_df = pd.DataFrame(0, index=cities, columns=cities)
    for index, row in trimmed_index_df.iterrows():
        # 先便利指标数据
        city = row['城市']
        # 监控过程
        print(f'正在处理{year}年{city}的迁入数据！')
        city_index = row[year]
        for index, row in in_out_df.iterrows():
            # 再遍历对应关系
            if row['年份'] != int(year):  # 如果年份对不上就不处理本行对应关系
                continue
            if row['地区A'] == city:  # 年份和城市都对应上了就继续分配
                out_city = row['地区B']
                in_city = city
                proportion = row['B迁入A占迁入A总人口的比值-年均值']
                # 计算对应的指标
                corresponding_index = city_index * proportion*0.01
                # 第一列是迁出城市，第一行是迁入城市
                now_network_df.loc[out_city, in_city] = corresponding_index
            else:
                # 城市没对应上
                continue
    return now_network_df


def migrate_index_trim_sum(input_df):
    input_df = input_df.drop(columns=['城市代码'])
    date_columns = input_df.columns[1:]  # 此时第一列是城市名称
    # 创建一个空的字典来存储每个年份的数据
    yearly_data = {}

    # 遍历所有日期列
    for col in date_columns:
        if isinstance(col, int):
            col = str(col)
        # 提取年份
        year = col[:4]

        # 如果年份还没有在字典中，初始化一个新的DataFrame
        if year not in yearly_data:
            yearly_data[year] = pd.DataFrame()

        # 将列数据添加到相应的年份DataFrame中
        yearly_data[year][int(col)] = input_df[int(col)]

    # 初始化一个新的DataFrame来存储最终的年度数据
    trimmed_df = pd.DataFrame(index=input_df.index)
    trimmed_df['城市'] = input_df['城市']  # 将城市列添加到新的DataFrame中

    # 计算每个年份的总和或平均值，并将结果添加到final_df中
    for year, data in yearly_data.items():
        # 计算年度总和或平均值
        trimmed_df[year] = data.mean(axis=1)  # 或者使用 .sum(axis=1) 来计算总和

    return trimmed_df


def storage_network_to_excel(networks):
    with pd.ExcelWriter('networks.xlsx') as writer:
        for name, network_df in networks:
            network_df.to_excel(writer, sheet_name=name, index=True)


if __name__ == '__main__':
    original_migrate_index_df = pd.read_excel('../scrawler/城市迁入规模指数.xlsx', engine='openpyxl', sheet_name='s1')
    # 将日期度量转化为年份度量并计算平均值
    trimmed_migrate_index_df = migrate_index_trim_sum(original_migrate_index_df)
    # 构建网络矩阵
    corresponding_in_out_df = pd.read_csv(
        '/Users/gaoxu/uni/科研/人口迁徙数据-城市间（2020-2023.10）/整理数据/百度迁徙-地区间-迁入迁出年度明细数据（2020.1-2023.11）.csv')
    corresponding_in_out_df = corresponding_in_out_df[['年份', '地区A', '地区B', 'B迁入A占迁入A总人口的比值-年均值']]
    #   得到指标年份和迁徙关系年份的交集
    years_in_index = trimmed_migrate_index_df.columns[1:]  # 含有指标的所有年份
    years_in_csv = corresponding_in_out_df['年份'].drop_duplicates().tolist()  # 有对应迁徙关系的所有年份
    set1 = set(str(int(year)) for year in years_in_csv if not math.isnan(year))  # 转换 set1 中的元素为字符串，并移除 nan
    set2 = set(years_in_index)
    intersection_year = set1.intersection(set2)
    years = list(intersection_year)
    years = sorted(years, key=lambda year: int(year))  # 将字符串列表作为数字进行排序，但保留字符串格式
    # 网络矩阵
    networks = []
    for year in years:
        this_year_index = trimmed_migrate_index_df[['城市', year]]
        tmp_network = network_construct(year, this_year_index, corresponding_in_out_df)
        networks.append((year, tmp_network))  # 用年份标度网络指标
    # 持久化存储
    storage_network_to_excel(networks)
