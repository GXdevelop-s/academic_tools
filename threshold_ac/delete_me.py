import pandas as pd

if __name__ == '__main__':
    path = '/Users/gaoxu/uni/科研/城市人口数据/城市大面板（加入城市所有人口）.xlsx'
    df = pd.read_excel(path)
    city_name = df['city_name'].tolist()
    distinct_names = set(city_name)
    print(len(distinct_names))
