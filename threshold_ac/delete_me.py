import pandas as pd

if __name__ == '__main__':
    path = 'pareto_coefficients.xlsx'
    df = pd.read_excel(path)
    city_name = df['Province'].tolist()
    distinct_names = set(city_name)
    print(len(distinct_names))
