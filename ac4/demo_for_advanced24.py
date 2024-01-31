import os
import re
from functools import reduce

import pandas as pd
from pandas.core.interchange import column

# 制造业二级分类
manufacturing_industries = ['农副食品加工业', '食品制造业', '酒、饮料和精制茶制造业', '烟草制品业', '纺织业',
                            '纺织服装、服饰业', '皮革、毛皮、羽毛及其制品和制鞋业', '木材加工和木、竹、藤、棕、草制品业',
                            '家具制造业', '造纸和纸制品业', '印刷和记录媒介复制业',
                            '文教、工美、体育和娱乐用品制造业', '石油、煤炭及其他燃料加工业',
                            '化学原料和化学制品制造业', '医药制造业', '化学纤维制造业', '橡胶和塑料制品业',
                            '非金属矿物制品业', '黑色金属冶炼和压延加工业', '有色金属冶炼和压延加工业',
                            '金属制品业', '通用设备制造业', '专用设备制造业', '汽车制造业',
                            '铁路、船舶、航空航天和其他运输设备制造业', '电气机械和器材制造业',
                            '计算机、通信和其他电子设备制造业', '仪器仪表制造业', '其他制造业',
                            '废弃资源综合利用业', '金属制品、机械和设备修理业']


# 判断时候为制造业，返回值为布尔值
def is_manufacture_industry(value):
    # 31个制造子行业
    manufacturing_industries = ['农副食品加工业', '食品制造业', '酒、饮料和精制茶制造业', '烟草制品业', '纺织业',
                                '纺织服装、服饰业', '皮革、毛皮、羽毛及其制品和制鞋业', '木材加工和木、竹、藤、棕、草制品业',
                                '家具制造业', '造纸和纸制品业', '印刷和记录媒介复制业',
                                '文教、工美、体育和娱乐用品制造业', '石油、煤炭及其他燃料加工业',
                                '化学原料和化学制品制造业', '医药制造业', '化学纤维制造业', '橡胶和塑料制品业',
                                '非金属矿物制品业', '黑色金属冶炼和压延加工业', '有色金属冶炼和压延加工业',
                                '金属制品业', '通用设备制造业', '专用设备制造业', '汽车制造业',
                                '铁路、船舶、航空航天和其他运输设备制造业', '电气机械和器材制造业',
                                '计算机、通信和其他电子设备制造业', '仪器仪表制造业', '其他制造业',
                                '废弃资源综合利用业', '金属制品、机械和设备修理业']
    return value in manufacturing_industries


# 对每一个excel进行处理
def data_analyse(file_path):
    print(file_path)
    cols = pd.read_excel(file_path, engine='openpyxl', nrows=1).columns.tolist()
    # 存在二级行业分类的excel
    if '二级行业分类' in cols:
        df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '二级行业分类'])  # 只取两列
        # 只要12-23年和31个制造子行业的数据
        filtered_df = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023) & df['二级行业分类'].apply(
                is_manufacture_industry)]
        # 要12-23年和所有行业的数据
        filtered_df2 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023)]
        # 建立行业为col和年份为index且初始元素都为0的dataframe
        index_years = list(range(2012, 2024))
        #  为避免每次都修改的是之前的列表
        columns_names = manufacturing_industries.copy()
        columns_names.append('年度制造业企业数量')
        columns_names.append('年度企业总量')
        result_df = pd.DataFrame(0, index=index_years, columns=columns_names)
        # 遍历符合要求的每行数据并用计数df进行计数
        for index, row in filtered_df.iterrows():
            year = int(row['成立日期'][:4])
            sub_industry = row['二级行业分类']
            result_df.at[year, sub_industry] += 1
            result_df.at[year, '年度制造业企业数量'] += 1
        # # filtered_df2中所有的企业都是符合要求的，不然
        for index, row in filtered_df2.iterrows():
            year = int(row['成立日期'][:4])
            result_df.at[year, '年度企业总量'] += 1
        return result_df
    # 没有二级行业分类只有所属行业的excel
    else:
        df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '所属行业'])  # 只取两列
        # 只要12-23年和31个制造子行业的数据
        filtered_df = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023) & df['所属行业'].apply(
                is_manufacture_industry)]
        # 要12-23年和所有行业的数据
        filtered_df2 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023)]
        # 建立行业为col和年份为index且初始元素都为0的dataframe
        index_years = list(range(2012, 2024))
        columns_names = manufacturing_industries.copy()
        columns_names.append('年度制造业企业数量')
        columns_names.append('年度企业总量')
        result_df = pd.DataFrame(0, index=index_years, columns=columns_names)
        # 遍历符合要求的每行数据并用计数df进行计数
        for index, row in filtered_df.iterrows():
            year = int(row['成立日期'][:4])
            sub_industry = row['所属行业']
            result_df.at[year, sub_industry] += 1
            result_df.at[year, '年度制造业企业数量'] += 1
            # # filtered_df2中所有的企业都是符合要求的，不然
        for index, row in filtered_df2.iterrows():
            year = int(row['成立日期'][:4])
            result_df.at[year, '年度企业总量'] += 1
        return result_df


def merge(df_list):
    column = df_list[0].columns.tolist()
    final_df = df_list[0]
    for i in range(1, len(df_list)):
        final_df = final_df[column] + df_list[i][column]
    return final_df


if __name__ == '__main__':
    directory_path = r'/Users/garrett/office_file/科研/工商业全量/数据/全国数据'
    all_files = os.listdir(directory_path)
    # 最终的dataframe
    df_list = []
    # 开始循环处理目录中的文件
    for file in all_files:
        if file.endswith('.xlsx'):
            # 文件绝对路径
            file_path = os.path.join(directory_path, file)
            # 数量矩阵
            result_df = data_analyse(file_path)
            if result_df.columns.duplicated().any():
                print(f"文件 {file} 的 DataFrame 存在重复列名")
            df_list.append(result_df)
        else:
            continue

    # 最终的dataframe
    final_df = pd.DataFrame(0, index=df_list[0].index, columns=df_list[0].columns)
    # 遍历所有 DataFrame，并累加到 final_df
    for df in df_list:
        if df.columns.duplicated().any():
            print("发现一个包含重复列名的 DataFrame")
        if not df.columns.equals(final_df.columns):
            print("发现一个列名或列顺序不一致的 DataFrame")
        try:
            final_df += df
        except ValueError as e:
            print("在累加过程中出错：", e)
            print("问题 DataFrame 的列名：", df.columns)
            break
    # 进行excel结果输出
    final_df.to_excel('final_result_further_year_details.xlsx')
    print('done!' * 3)
