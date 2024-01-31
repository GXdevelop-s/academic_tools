import os
import re
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
        # 计算企业总数量
        count = len(filtered_df)
        # 建立行业为col和年份为index且初始元素都为0的dataframe
        index_years = list(range(2012, 2024))
        columns_names = manufacturing_industries
        result_df = pd.DataFrame(0, index=index_years, columns=columns_names)
        # 遍历符合要求的每行数据并用计数df进行计数
        for index, row in filtered_df.iterrows():
            year = int(row['成立日期'][:4])
            sub_industry = row['二级行业分类']
            result_df.at[year, sub_industry] += 1
        # 对result_df的每一行求和,计算当前城市的年度制造业总量
        result_df['年度制造业总量'] = result_df.sum(axis=1)
        return result_df, count
    # 没有二级行业分类只有所属行业的excel
    else:
        df = pd.read_excel(file_path, engine='openpyxl', usecols=['成立日期', '所属行业'])  # 只取两列
        # 只要12-23年和31个制造子行业的数据
        filtered_df = df[
            df['成立日期'].str[:4].fillna('0').astype(int).between(2012, 2023) & df['所属行业'].apply(
                is_manufacture_industry)]
        # 计算企业总数量
        count = len(filtered_df)
        # 建立行业为col和年份为index且初始元素都为0的dataframe
        index_years = list(range(2012, 2024))
        columns_names = manufacturing_industries
        result_df = pd.DataFrame(0, index=index_years, columns=columns_names)
        # 遍历符合要求的每行数据并用计数df进行计数
        for index, row in filtered_df.iterrows():
            year = int(row['成立日期'][:4])
            sub_industry = row['所属行业']
            result_df.at[year, sub_industry] += 1
        # 对result_df的每一行求和,计算当前城市的年度制造业总量
        result_df['年度制造业总量'] = result_df.sum(axis=1)
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
    city_list[-1].result_df = city_list[-1].result_df + result_df  # 最新加入的城市的dataframe和其后续的excel表的df对应元素相加
    city_list[-1].count = city_list[-1].count + count


# 存储到excel中
def save_as_excel():
    with pd.ExcelWriter('test_result.xlsx', engine='openpyxl') as writer:
        startrow = 0
        for idx, city in enumerate(city_list):

            # 将city_name写入到当前的startrow位置
            ws = writer.sheets['Sheet1'] if 'Sheet1' in writer.sheets else None
            if not ws:
                ws = writer.book.create_sheet('Sheet1')
            ws.cell(row=startrow + 1, column=1, value=city.city_name)

            # 对每个城市的12-23年11年制造业总量求和
            # ws.cell(row=startrow + 1, column=2, value='2012-2023年制造业总量')
            # ws.cell(row=startrow + 1, column=3, value=city.count)

            # 如果是第一个DataFrame，写入header
            if idx == 0:
                header = True
            else:
                header = False

            # 更新startrow为city_name之后的行，并将DataFrame写入到这个位置
            startrow += 1
            city.result_df.to_excel(writer, sheet_name='Sheet1', startrow=startrow, index=True, header=header)

            # 更新下一个dataframe的起始行，包括DataFrame本身的长度和一个额外的行为下一个city_name预留的位置
            startrow += city.result_df.shape[0] + 1


if __name__ == '__main__':
    # 用以区别是否为一同城市的不同数据表
    city_flag = False  # 默认是不同的城市
    last_city = ''
    city_list = []  # 所有城市对象的容器
    directory_path = r'/Users/garrett/office_file/科研/工商业全量/数据/测试数据'
    all_files = os.listdir(directory_path)

    # 开始循环处理目录中的文件
    for file in all_files:
        # 检查城市是否已经有存在的数据了，并调整city_flag
        last_city = check_cities(file)
        # 文件绝对路径
        file_path = os.path.join(directory_path, file)
        # 数量矩阵
        result_df, count = data_analyse(file_path)
        if city_flag:  # 不同的excel，相同的城市,进行df对应元素相加
            city_merge(result_df, count)
        else:
            # 新的城市，创建对象，并加入城市列表
            temp_city = City(last_city, result_df, count)
            city_list.append(temp_city)

    # 进行excel结果输出
    save_as_excel()
    print('done!')
    #   进行 时间优化，然后开始运行
