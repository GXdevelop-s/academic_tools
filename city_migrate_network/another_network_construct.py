import pandas as pd


def construct_network(original_df, s_cities_unique, year):
    now_network = pd.DataFrame(0, index=s_cities_unique, columns=s_cities_unique)
    for index, row in original_df.iterrows():
        if row['年份'] != year:
            continue
        now_network.loc[row['始发城市'], row['终点城市']] = row['年度实际迁徙指数']
    return now_network


def storage_network_to_excel(networks):
    with pd.ExcelWriter('another_networks.xlsx') as writer:
        for name, network_df in networks:
            print(f'正在处理{name}')
            sheet_name = str(name)
            network_df.to_excel(writer, sheet_name=sheet_name, index=True)


if __name__ == '__main__':
    original_df = pd.read_csv(
        '/Users/gaoxu/resources/人口迁徙规模数据-367个城市（2018-2023年）/人口迁徙-年度明细数据（2018.6-2023.12）.csv')
    start_city_series = original_df['始发城市']
    # 去除城市列表的nan并去重
    s_cities_unique = start_city_series.dropna().drop_duplicates()
    # 获取所有年份
    year_series = original_df['年份']
    year_list = year_series.dropna().drop_duplicates()
    networks = []
    for year in year_list:
        # 构造网络
        this_network = construct_network(original_df, s_cities_unique, year)
        networks.append((year, this_network))
    # 持久化存储
    storage_network_to_excel(networks)
