import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('result.xlsx')
    province = df['province']
    single_province = list(set(province))
    print(len(single_province))
