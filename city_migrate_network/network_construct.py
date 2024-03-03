import pandas as pd


def network_construct(year, trimmed_index_df, in_out_df):
    # 初始化城市迁移矩阵
    cities = trimmed_index_df['城市'].tolist()
    now_network_df = pd.DataFrame(0, index=cities, columns=cities)
    print('ok')
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
        trimmed_df[year] = data.mean(axis=1)  # 或者使用 .sun(axis=1) 来计算总和

    return trimmed_df


if __name__ == '__main__':
    original_migrate_index_df = pd.read_excel('../scrawler/城市迁入规模指数.xlsx', engine='openpyxl', sheet_name='s1')
    trimmed_migrate_index_df = migrate_index_trim_sum(original_migrate_index_df)
    # 构建网络矩阵
    years = trimmed_migrate_index_df.columns[1:]
    corresponding_in_out_df = pd.read_csv(
        '/Users/gaoxu/uni/科研/人口迁徙数据-城市间（2020-2023.10）/整理数据/百度迁徙-地区间-迁入迁出年度明细数据（2020.1-2023.11）.csv')
    # 网络矩阵
    networks = []
    for year in years:
        this_year_index = trimmed_migrate_index_df[['城市', year]]
        tmp_network = network_construct(year, this_year_index, corresponding_in_out_df)
        networks.append(tmp_network)
