import pandas as pd

if __name__ == '__main__':
    file_path = r'final_result2.0.xlsx'
    excel_date = pd.read_excel(file_path, engine='openpyxl')
    print(len(excel_date))
    print(excel_date.head(20))
