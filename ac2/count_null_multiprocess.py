import os
import time

import pandas as pd
from concurrent.futures import ProcessPoolExecutor

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
    return value in manufacturing_industries

# 处理单个excel，当成立日期中没有2022年时，返回布尔值False，当有时返回注册资本非空的22年制造业企业数量
def data_analyse(file_path):
    print(file_path)
    # 判断当前excel有没有2022
    test_df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期'])
    # 指定要检查的列和要查找的子字符串
    column_name = '成立日期'
    search_substring = '2022'
    # 判断列是否包含特定子字符串
    contains_substring = any(test_df[column_name].astype(str).str.contains(search_substring))

    # 包含子字符串
    if contains_substring:
        # 查看改excel的列名
        cols = pd.read_excel(file_path, engine='openpyxl', nrows=1).columns.tolist()
        # 存在二级行业分类的excel
        if '二级行业分类' in cols:
            df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '二级行业分类', '注册资本'])  # 只取需要的列
            # 只要22年和31个制造子行业的数据
            filtered_df = df[
                (df['成立日期'].str[:4].fillna('0') == '2022') & df['二级行业分类'].apply(
                    is_manufacture_industry)]
            # 计算2022年成立的注册资本非空的制造业企业总数量
            count = filtered_df['注册资本'].count()
            return count
        # 没有二级行业分类只有所属行业的excel
        else:
            df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '所属行业', '注册资本'])  # 只取两列
            # 只要22年和31个制造子行业的数据
            filtered_df = df[
                (df['成立日期'].str[:4].fillna('0') == '2022') & df['所属行业'].apply(
                    is_manufacture_industry)]
            # 计算2022年成立的注册资本非空的制造业企业总数量
            count = filtered_df['注册资本'].count()
            return count
    # 不包含子字符串
    else:
        # 返回Fales，代表无子字符串
        return False


if __name__ == '__main__':
    start_time = time.time()
    directory_path = r'G:\中国工商注册企业全量信息（2023.9更新）\全国数据'
    all_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]

    final_num = 0

    # 使用多进程处理
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(data_analyse, all_files))

    # 统计结果
    for result in results:
        if result is False:
            continue
        else:
            final_num += result
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('2022年注册资本非空的制造业企业数量为{}\n'.format(final_num) * 3)
    print(f"程序运行时间: {elapsed_time} 秒")
