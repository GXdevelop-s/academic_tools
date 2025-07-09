import os
import time
import pandas as pd


def generate_province_city(excel_file_path):
    excel_data_needed = pd.read_excel(excel_file_path, engine='openpyxl', sheet_name='337个地级以上行政单位（两步法sum）',
                                      skiprows=1, usecols=['province', 'city_name'])
    # 找到了正确的省份和city_name的对应关系，乱序
    '''
    province  city_name
    四川省        巴中市              
    '''
    province_city_df = excel_data_needed

    return province_city_df


def init_result_df(p_c_df):
    # 创建年份 DataFrame
    years = pd.DataFrame({'年份': range(2000, 2024)})

    # 进行笛卡尔积合并
    merged_df = pd.merge(p_c_df, years, how='cross')

    # 添加 'a' 列和 'b' 列，这里使用 NaN 作为示例，您可以根据需要替换
    merged_df['城市区域人口数量'] = 0
    merged_df['城市人口总量'] = 0
    '''
    # 最终的df结构
    province  city_name  年份   城市区域人口数量      城市人口总量
    xx             ss      2019         187267          238976
    '''
    return merged_df


def process_csvs(csv_list, csv_dir, p_c_df):
    # 计数器
    count = 0
    # 初始化结果df
    result_df = init_result_df(p_c_df)
    # 先对csv_list按照年份升序排序
    print(csv_list)
    csv_list.sort(key=lambda file_name: int(file_name[-8:-4]))
    # 循环处理每一个csv
    for file_name in csv_list:
        # 拼接csv完整路径
        file_path = os.path.join(csv_dir, file_name)
        count += 1
        print(f'Processing No.{count}: {file_name}')
        # 城市总人口的数据进城市总人口的，城市城市区域的进城市区域的处理逻辑，依靠result_df到处向自己写入数据，进行数据流转（有了这个excel，就只需要将所有的csv放一块就可以了）
        if file_name.startswith('urban'):
            # print('urban')
            result_df = process_urban_csv(file_path, result_df, p_c_df)
        elif file_name.startswith('full'):
            # print('full')
            result_df = process_full_csv(file_path, result_df, p_c_df)
    # 最终返回结果
    return result_df


def process_urban_csv(file_path, result_df_input, p_c_df):
    csv_df = pd.read_csv(file_path)
    # 判断csv所属的年份数据
    year = int(file_path[-8:-4])
    # csv格式
    '''
    OBJECTID    地名      ZONE_CODE    COUNT     AREA      MIN     MAX     RANGE      MEAN        STD           SUM     VARIETY     MAJORITY     MINORITY       MEDIAN     
        1     阿苏克地区       1       196851   13.670208    0     28336    28336     12.7495     193.766    1509756.000   1021          0           194             0
    '''
    filtered_csv_df = csv_df[['地名', 'SUM']]
    # 根据p_c_df对于csv的城市名称进行修复：
    for index, row in filtered_csv_df.iterrows():
        if len(row['地名']) > 7:
            for city in p_c_df['city_name'].values:
                if city.startswith(row['地名']):
                    row['地名'] = city
        else:
            continue

    # 定义一个内部函数用于处理filtered_csv_df的每一行
    def process_row(row, year):
        city = row['地名']
        # 开始赋值
        population = row['SUM']
        result_df_input.loc[
            (result_df_input['city_name'] == city) & (result_df_input['年份'] == year), '城市区域人口数量'] = population

    # 开始应用内部函数
    filtered_csv_df = filtered_csv_df.copy()
    filtered_csv_df.apply(lambda row: process_row(row, year), axis=1)
    # 这样处理完就可以输出返回了
    result_df_output = result_df_input
    return result_df_output


def process_full_csv(file_path, result_df_input, p_c_df):
    csv_df = pd.read_csv(file_path)
    # 判断csv所属的年份数据
    year = int(file_path[-8:-4])
    # csv格式
    '''
    OBJECTID    地名      ZONE_CODE    COUNT     AREA      MIN     MAX     RANGE      MEAN        STD           SUM     VARIETY     MAJORITY     MINORITY       MEDIAN     
        1     阿苏克地区       1       196851   13.670208    0     28336    28336     12.7495     193.766    1509756.000   1021          0           194             0
    '''
    # 只需要城市名和人口数这两列
    filtered_csv_df = csv_df[['地名', 'SUM']]
    # 根据p_c_df对于csv的城市名称进行修复：
    for index, row in filtered_csv_df.iterrows():
        if len(row['地名']) > 7:
            for city in p_c_df['city_name'].values:
                if city.startswith(row['地名']):
                    row['地名'] = city

    # 定义一个内部函数用于处理filtered_csv_df的每一行
    def process_row(row, year):
        city = row['地名']
        # 开始赋值
        population = row['SUM']
        result_df_input.loc[
            (result_df_input['city_name'] == city) & (result_df_input['年份'] == year), '城市人口总量'] = population

    # 开始应用内部函数
    filtered_csv_df = filtered_csv_df.copy()
    filtered_csv_df.apply(lambda row: process_row(row, year), axis=1)
    # 这样处理完就可以输出返回了
    result_df_output = result_df_input

    return result_df_output


def add_rank(df):
    # rank(method='dense', ascending=False) 表示排名是按照城市人口总量降序排列的，且排名方式为“dense”，即排名连续，
    df['rank'] = df.groupby('年份')['城市区域人口数量'].rank(method='dense', ascending=False)   # 按照城市人口总量进行排序
    return df


if __name__ == '__main__':
    '''
    csv命名规范：如果是城视区域的csv 必须以   urban  开头
                如果是城市总区域的csv 必须以 full开头
    '''
    start_time = time.time()
    excel_file_path = r'/Users/gaoxu/uni/科研/城市人口数据/333个地级市名单+4个直辖市=337个地级以上行政区划（20210110）.xlsx'
    csv_file_dir = r'/Users/gaoxu/uni/科研/城市人口数据/outputs'
    # 得到省份-城市的对应关系（以df表示）
    province_city_df = generate_province_city(excel_file_path=excel_file_path)
    # 读入所有的csv文件
    all_csv_files = os.listdir(csv_file_dir)
    # 清洗除了csv以外的其它文件
    all_csv_files = [file for file in all_csv_files if file.endswith('.csv')]
    # 处理所有文件,并传入省市关系，得到最终结果，
    final_result_df = process_csvs(all_csv_files, csv_file_dir, province_city_df)
    # 按照 'province' 和 'city' 列进行排序
    final_result_df.sort_values(by=['province', 'city_name'], inplace=True)
    # 由于zipf‘s law的要求添加rank列
    final_result_df_with_rank = add_rank(final_result_df)
    # 输出成excel
    final_result_df.to_excel("output城市区域（加2023年）.xlsx", index=False)
    end_time = time.time()
    execute_time = end_time - start_time
    print('done!\n' * 3)
    print(f'程序用时：{execute_time}秒')