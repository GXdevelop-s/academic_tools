import pandas as pd

if __name__ == '__main__':
    original_df = pd.read_csv(
        '/Users/gaoxu/resources/人口迁徙规模数据-367个城市（2018-2023年）/人口迁徙-年度明细数据（2018.6-2023.12）.csv')
    start_city_series = original_df['始发城市']
    # 去除nan并去重
    s_cities_unique = start_city_series.dropna().drop_duplicates()
    print(s_cities_unique)
