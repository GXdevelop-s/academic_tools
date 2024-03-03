import pandas as pd


def network_construct():
    pass


def migrate_index_trim_sum(input_df):
    input_df = input_df.drop(columns=['城市代码'])
    # 已知年份和城市
    # years = [2019, 2020, 2021, 2022, 2023, 2024]
    # cities = input_df['城市'].unique().tolist()
    # 准备年份城市数据
    # data = {year: {city: 0 for city in cities} for year in years}
    # 获取除城市名称外的所有列名
    date_columns = input_df.columns[1:]  # 假设第一列是城市名称
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
    final_df = pd.DataFrame(index=input_df.index)
    final_df['城市'] = input_df['城市']  # 将城市列添加到新的DataFrame中

    # 计算每个年份的总和或平均值，并将结果添加到final_df中
    for year, data in yearly_data.items():
        # 计算年度总和或平均值
        final_df[year] = data.mean(axis=1)  # 或者使用 .mean(axis=1) 来计算平均值

    return final_df





if __name__ == '__main__':
    original_migrate_index_df = pd.read_excel('../scrawler/城市迁入规模指数.xlsx', engine='openpyxl', sheet_name='s1')
    trimmed_migrate_index_df = migrate_index_trim_sum(original_migrate_index_df)
    print(trimmed_migrate_index_df)
