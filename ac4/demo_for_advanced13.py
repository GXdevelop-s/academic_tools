import os
import re
import time

import pandas as pd

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
# 分企业类型制造业二级分类
manufacturing_industries_expanded = [
    '农副食品加工业', '农副食品加工业(有限责任公司)', '农副食品加工业(个体工商户)',
    '食品制造业', '食品制造业(有限责任公司)', '食品制造业(个体工商户)',
    '酒、饮料和精制茶制造业', '酒、饮料和精制茶制造业(有限责任公司)', '酒、饮料和精制茶制造业(个体工商户)',
    '烟草制品业', '烟草制品业(有限责任公司)', '烟草制品业(个体工商户)',
    '纺织业', '纺织业(有限责任公司)', '纺织业(个体工商户)',
    '纺织服装、服饰业', '纺织服装、服饰业(有限责任公司)', '纺织服装、服饰业(个体工商户)',
    '皮革、毛皮、羽毛及其制品和制鞋业', '皮革、毛皮、羽毛及其制品和制鞋业(有限责任公司)',
    '皮革、毛皮、羽毛及其制品和制鞋业(个体工商户)',
    '木材加工和木、竹、藤、棕、草制品业', '木材加工和木、竹、藤、棕、草制品业(有限责任公司)',
    '木材加工和木、竹、藤、棕、草制品业(个体工商户)',
    '家具制造业', '家具制造业(有限责任公司)', '家具制造业(个体工商户)',
    '造纸和纸制品业', '造纸和纸制品业(有限责任公司)', '造纸和纸制品业(个体工商户)',
    '印刷和记录媒介复制业', '印刷和记录媒介复制业(有限责任公司)', '印刷和记录媒介复制业(个体工商户)',
    '文教、工美、体育和娱乐用品制造业', '文教、工美、体育和娱乐用品制造业(有限责任公司)',
    '文教、工美、体育和娱乐用品制造业(个体工商户)',
    '石油、煤炭及其他燃料加工业', '石油、煤炭及其他燃料加工业(有限责任公司)', '石油、煤炭及其他燃料加工业(个体工商户)',
    '化学原料和化学制品制造业', '化学原料和化学制品制造业(有限责任公司)', '化学原料和化学制品制造业(个体工商户)',
    '医药制造业', '医药制造业(有限责任公司)', '医药制造业(个体工商户)',
    '化学纤维制造业', '化学纤维制造业(有限责任公司)', '化学纤维制造业(个体工商户)',
    '橡胶和塑料制品业', '橡胶和塑料制品业(有限责任公司)', '橡胶和塑料制品业(个体工商户)',
    '非金属矿物制品业', '非金属矿物制品业(有限责任公司)', '非金属矿物制品业(个体工商户)',
    '黑色金属冶炼和压延加工业', '黑色金属冶炼和压延加工业(有限责任公司)', '黑色金属冶炼和压延加工业(个体工商户)',
    '有色金属冶炼和压延加工业', '有色金属冶炼和压延加工业(有限责任公司)', '有色金属冶炼和压延加工业(个体工商户)',
    '金属制品业', '金属制品业(有限责任公司)', '金属制品业(个体工商户)',
    '通用设备制造业', '通用设备制造业(有限责任公司)', '通用设备制造业(个体工商户)',
    '专用设备制造业', '专用设备制造业(有限责任公司)', '专用设备制造业(个体工商户)',
    '汽车制造业', '汽车制造业(有限责任公司)', '汽车制造业(个体工商户)',
    '铁路、船舶、航空航天和其他运输设备制造业', '铁路、船舶、航空航天和其他运输设备制造业(有限责任公司)',
    '铁路、船舶、航空航天和其他运输设备制造业(个体工商户)',
    '电气机械和器材制造业', '电气机械和器材制造业(有限责任公司)', '电气机械和器材制造业(个体工商户)',
    '计算机、通信和其他电子设备制造业', '计算机、通信和其他电子设备制造业(有限责任公司)',
    '计算机、通信和其他电子设备制造业(个体工商户)',
    '仪器仪表制造业', '仪器仪表制造业(有限责任公司)', '仪器仪表制造业(个体工商户)',
    '其他制造业', '其他制造业(有限责任公司)', '其他制造业(个体工商户)',
    '废弃资源综合利用业', '废弃资源综合利用业(有限责任公司)', '废弃资源综合利用业(个体工商户)',
    '金属制品、机械和设备修理业', '金属制品、机械和设备修理业(有限责任公司)', '金属制品、机械和设备修理业(个体工商户)'
]


# 城市类
class City:
    def __init__(self, city_name, result_df, count):
        self.city_name = city_name
        self.result_df = result_df
        self.result_df.index.name = city_name  # 给这个城市的df标注城市名称
        self.count = count  # 12-23年该城市的制造业企业总数


# 判断时候为制造业，返回值为布尔值
def is_manufacture_industry(value):
    # 31个制造子行业
    global manufacturing_industries
    return value in manufacturing_industries


# 从Excel文件名中分离出省份和城市
def check_location(file):
    # 使用正则表达式匹配省份和城市
    match = re.match(r'([\u4e00-\u9fff]+)_.*?([\u4e00-\u9fff]+)', file)

    # 如果匹配成功，则提取省份和城市
    if match:
        province = match.group(1)
        city = match.group(2)
    else:
        submatch = re.match(r'^[\u4e00-\u9fff]+', file)
        province = submatch.group()
        city = province
    return province, city


# 对每一个excel进行处理
def data_analyse(file_path, file):
    print(file_path)
    cols = pd.read_excel(file_path, engine='openpyxl', nrows=1).columns.tolist()
    # 存在二级行业分类的excel
    if '二级行业分类' in cols:
        df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '二级行业分类', '企业类型'])  # 只取两列
        # 只要12-23年和31个制造子行业的数据
        filtered_df1 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023) & df['二级行业分类'].apply(
                is_manufacture_industry)]
        # 要12-23年和所有行业的数据
        filtered_df2 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023)]
        # 计算企业总数量，这个数字没什么用
        count = len(filtered_df1)
        # 构造符合面板数据的DataFrame,之前加入省份城市年份，之前加入个体工商户和有限责任公司及其之和这三列
        index_years = list(range(2012, 2024))
        columns_names = ['省份', '城市', '年份']
        columns_names.extend(manufacturing_industries_expanded)
        columns_names.append('有限责任公司')
        columns_names.append('个体工商户')
        columns_names.append('有限责任公司+个体工商户')
        columns_names.append('年度制造业企业总量')
        columns_names.append('年度企业总量')
        result_df = pd.DataFrame(index=index_years, columns=columns_names)
        # 获取当前处理文件的省份城市，并直接按照面板数据的原则赋值给第一、二、三列
        province, city = check_location(file)
        result_df['省份'] = province
        result_df['城市'] = city
        result_df['年份'] = index_years
        # 找出除了 '省份'、'城市'、'年份' 之外的所有列
        columns_to_fill = [col for col in result_df.columns if col not in ['省份', '城市', '年份']]
        # 为这些列赋值0
        result_df[columns_to_fill] = 0

        # 定义一个内部函数，用于处理”企业类型这一列“
        def filt_enterprise_type(etype):
            if isinstance(etype, str):
                # 如果企业类型为“个体工商户”，则保持不变
                if etype == '个体工商户':
                    return etype
                # 如果企业类型的前六个字符为“有限责任公司”，则只保留这六个字符
                elif etype.startswith('有限责任公司'):
                    return '有限责任公司'
                # 其他情况下，保持原状
                else:
                    return etype
            else:
                return etype

        # 定义一个内部函数，用于处理filtered_df1每一行
        def process_row1(row):
            year = int(row['成立日期'][:4])
            sub_industry = row['二级行业分类']
            enterprise_type = row['企业类型']  # 只有两种 —— 有限公司、个体工商户
            # 构建完整的列名，格式为"二级行业分类(企业类型)"
            full_column_name = f'{sub_industry}({enterprise_type})'
            # 只有构造出来的full_column_name在列名中才可以，也就是用这个构建出的列名完成了两个匹配要求
            if full_column_name in result_df.columns:
                result_df.at[year, full_column_name] += 1
                result_df.at[year, row['企业类型']] += 1
                result_df.at[year, '有限责任公司+个体工商户'] += 1
            # 无论是制造业哪个子行业，都是制造业
            result_df.at[year, '年度制造业企业总量'] += 1
            # 每一个二级行业分类（全企业类型，包括但不限于有限公司、个体工商户）
            result_df.at[year, row['二级行业分类']] += 1

        # 定义一个内部函数，用于处理filtered_df2每一行
        def process_row2(row):
            # 因为filtered_df2的所有企业都是符合时间要求的，所以，只需要放到正确的行（年份）
            year = int(row['成立日期'][:4])
            result_df.at[year, '年度企业总量'] += 1

        # 预先处理filtered_df1的企业类型这一列
        filtered_df1 = filtered_df1.copy()  # 创建一个副本以避免 SettingWithCopyWarning
        filtered_df1['企业类型'] = filtered_df1['企业类型'].apply(filt_enterprise_type)
        # 对filtered_df1应用函数进行迭代
        filtered_df1.apply(process_row1, axis=1)
        # 为filtered_df2创建一个副本
        filtered_df2 = filtered_df2.copy()  # 创建一个副本以避免 SettingWithCopyWarning
        # 对filtered_df2应用函数进行迭代
        filtered_df2.apply(process_row2, axis=1)

        return result_df, count
    # 没有二级行业分类只有所属行业的excel
    else:
        df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '所属行业', '企业类型'])  # 只取两列
        # 只要12-23年和31个制造子行业的数据
        filtered_df1 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023) & df['所属行业'].apply(
                is_manufacture_industry)]
        # 要12-23年和所有行业的数据
        filtered_df2 = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023)]

        # 计算企业总数量，这个数字没什么用
        count = len(filtered_df1)
        # 构造符合面板数据的DataFrame,之前加入省份城市年份，之前加入个体工商户和有限责任公司及其之和这三列
        index_years = list(range(2012, 2024))
        columns_names = ['省份', '城市', '年份']
        columns_names.extend(manufacturing_industries_expanded)
        columns_names.append('有限责任公司')
        columns_names.append('个体工商户')
        columns_names.append('有限责任公司+个体工商户')
        columns_names.append('年度制造业企业总量')
        columns_names.append('年度企业总量')
        result_df = pd.DataFrame(index=index_years, columns=columns_names)
        # 获取当前处理文件的省份城市，并直接按照面板数据的原则赋值给第一、二、三列
        province, city = check_location(file)
        result_df['省份'] = province
        result_df['城市'] = city
        result_df['年份'] = index_years
        # 找出除了 '省份'、'城市'、'年份' 之外的所有列
        columns_to_fill = [col for col in result_df.columns if col not in ['省份', '城市', '年份']]
        # 为这些列赋值0
        result_df[columns_to_fill] = 0

        # 定义一个内部函数，用于处理”企业类型这一列“
        def filt_enterprise_type(etype):
            # 如果企业类型为“个体工商户”，则保持不变
            if etype == '个体工商户':
                return etype
            # 如果企业类型的前六个字符为“有限责任公司”，则只保留这六个字符
            elif etype.startswith('有限责任公司'):
                return '有限责任公司'
            # 其他情况下，保持原状
            else:
                return etype

        # 定义一个内部函数，用于处理每一行
        def process_row1(row):
            year = int(row['成立日期'][:4])
            sub_industry = row['所属行业']
            enterprise_type = row['企业类型']
            # 构建完整的列名，格式为"二级行业分类(企业类型)"
            full_column_name = f'{sub_industry}({enterprise_type})'
            # 只有构造出来的full_column_name在列名中才可以，也就是用这个构建出的列名完成了两个匹配要求
            if full_column_name in result_df.columns:
                result_df.at[year, full_column_name] += 1
                result_df.at[year, row['企业类型']] += 1
                result_df.at[year, '有限责任公司+个体工商户'] += 1
            # 无论是制造业哪个子行业，都是制造业
            result_df.at[year, '年度制造业企业总量'] += 1
            # 每一个所属行业（全企业类型，包括但不限于有限公司、个体工商户）
            result_df.at[year, row['所属行业']] += 1

        # 定义一个内部函数，用于处理filtered_df2每一行
        def process_row2(row):
            # 因为filtered_df2的所有企业都是符合时间要求的，所以，只需要放到正确的行（年份）
            year = int(row['成立日期'][:4])
            result_df.at[year, '年度企业总量'] += 1

        # 预先处理filtered_df1的企业类型这一列
        filtered_df1 = filtered_df1.copy()  # 创建一个副本以避免 SettingWithCopyWarning
        filtered_df1['企业类型'] = filtered_df1['企业类型'].apply(filt_enterprise_type)
        # 对filtered_df1应用函数进行迭代
        filtered_df1.apply(process_row1, axis=1)
        # 为filtered_df2创建一个副本
        filtered_df2 = filtered_df2.copy()  # 创建一个副本以避免 SettingWithCopyWarning
        # 对filtered_df2应用函数进行迭代
        filtered_df2.apply(process_row2, axis=1)

        return result_df, count


# 城市名称检查,返回值为该次的城市名，将作为下一次检查的lastcity
def check_cities(file):
    global city_flag  # 声明全局变量
    global last_city
    # 提取城市名
    simplified_name = ''.join(re.findall(r'[\u4e00-\u9fa5]', file))
    if last_city != simplified_name:
        city_flag = False
        last_city = simplified_name
    else:
        city_flag = True
    return last_city


# 相同城市，对应元素合并
def city_merge(result_df, count):
    global city_list
    to_add_col_list = manufacturing_industries_expanded + ['有限责任公司', '个体工商户', '有限责任公司+个体工商户',
                                                           '年度制造业企业总量', '年度企业总量']
    city_list[-1].result_df[to_add_col_list] = city_list[-1].result_df[to_add_col_list] + result_df[
        to_add_col_list]  # 最新加入的城市的dataframe和其后续的excel表的df对应元素相加
    city_list[-1].count = city_list[-1].count + count


# 存储到excel中
def save_as_excel():
    with pd.ExcelWriter('final_result_further_details.xlsx', engine='openpyxl') as writer:
        startrow = 0
        for idx, city in enumerate(city_list):
            # 如果是第一个DataFrame，写入header
            if idx == 0:
                header = True
                city.result_df.to_excel(writer, sheet_name='Sheet1', startrow=startrow, index=False, header=header)

                # 更新下一个dataframe的起始行，包括DataFrame本身的长度和一个额外的行为下一个city_name预留的位置和col_name的单独一行
                startrow += city.result_df.shape[0] + 1
                continue
            else:
                header = False
            city.result_df.to_excel(writer, sheet_name='Sheet1', startrow=startrow, index=False, header=header)
            # 更新下一个dataframe的起始行，包括DataFrame本身的长度和一个额外的行为下一个city_name预留的位置
            startrow += city.result_df.shape[0]


if __name__ == '__main__':
    start_time = time.time()
    # 用以区别是否为一同城市的不同数据表
    city_flag = False  # 默认是不同的城市
    last_city = ''
    city_list = []  # 所有城市对象的容器
    directory_path = r'/Users/garrett/office_file/科研/工商业全量/数据/全国数据'
    all_files = os.listdir(directory_path)
    # 在Macos中，默认的文件读取顺序是基于文件在文件系统节点中的位置，而非像windos中的那样按照字典顺序被读取，所以排序
    all_files.sort()
    # 开始循环处理目录中的文件
    for file in all_files:
        if file.endswith('.xlsx'):
            # 检查城市是否已经有存在的数据了，并调整city_flag
            last_city = check_cities(file)
            # 文件绝对路径
            file_path = os.path.join(directory_path, file)
            # 数量矩阵
            result_df, count = data_analyse(file_path, file)
            if city_flag:  # 不同的excel，相同的城市,进行df对应元素相加
                city_merge(result_df, count)
            else:
                # 新的城市，创建对象，并加入城市列表
                temp_city = City(last_city, result_df, count)
                city_list.append(temp_city)
        else:
            continue
    # 进行excel结果输出
    save_as_excel()
    print('done!\n' * 3)
    end_time = time.time()
    print(f'程序的运行时间为{end_time - start_time}秒')
