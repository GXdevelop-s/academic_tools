from pathlib import Path
import re
import pandas as pd


def yearly_employment(path):
    try:
        df = pd.read_csv(
            path,
            encoding="gb18030",
            engine="python",
            sep=None,
            on_bad_lines="skip",
            dtype=str
        )
    except UnicodeDecodeError:
        # 重新读取时忽略无法解码的字符
        import io

        with open(path, "rb") as f:
            text = f.read().decode("gb18030", errors="replace")
        df = pd.read_csv(
            io.StringIO(text),
            engine="python",  # 默认的 c 高速解析器快但是严格，python能自动推断分隔符
            sep=None,
            on_bad_lines="skip",  # 遇到解析失败的行默认的是报错，改成静默跳过
            dtype=str,
            usecols=['企业名称', '招聘岗位', '工作城市', '工作区域', '招聘发布日期', '招聘结束日期']
        )
    print(df.shape)

    # === 清洗列名、去空格 ===
    df.columns = [c.strip().replace("\ufeff", "") for c in df.columns]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()

    # === 解析日期 ===
    df['招聘发布日期'] = pd.to_datetime(df['招聘发布日期'], errors='coerce')
    df['招聘结束日期'] = pd.to_datetime(df['招聘结束日期'], errors='coerce')

    # === 去重：相同岗位（4键）取最早发布、最晚结束 ===
    keys = ['企业名称', '招聘岗位', '工作城市', '工作区域']
    jobs = (df.groupby(keys, as_index=False)
            .agg(招聘发布日期=('招聘发布日期', 'min'),
                 招聘结束日期=('招聘结束日期', 'max')))

    # === 生成发布事件 + 结束事件 ===
    events = []

    pub = jobs.dropna(subset=['招聘发布日期']).copy()
    pub['year'] = pub['招聘发布日期'].dt.year.astype('Int64')
    pub['month'] = pub['招聘发布日期'].dt.month.astype('Int64')
    pub['city'] = pub['工作城市']
    pub['delta'] = 1
    events.append(pub[['year', 'month', 'city', 'delta']])

    # === NEW: 拆分多城市“合肥市/郑州市/…”并展开 ===
    events_df = pd.concat(events, ignore_index=True)

    sep_pat = r'[\/、,，;；\s]+'

    def split_cities(x: str):
        if pd.isna(x) or str(x).strip() == "":
            return []
        parts = re.split(sep_pat, str(x))
        return [p.strip() for p in parts if p.strip() != ""]

    events_df['city_list'] = events_df['city'].apply(split_cities)
    events_df = events_df.explode('city_list', ignore_index=True)
    events_df = events_df.dropna(subset=['city_list'])

    # 关键改动：用 city_list 覆盖原 city，然后删除 city_list，避免重名
    events_df['city'] = events_df['city_list']
    events_df = events_df.drop(columns=['city_list'])

    # （可选）统一城市名：去掉末尾“市”
    events_df['city'] = events_df['city'].str.replace(r'市$', '', regex=True).str.strip()

    # 只保留需要的列（确保唯一的 city 列存在）
    events_df = events_df[['year', 'month', 'city', 'delta']]
    # === 聚合：year, month, city, nums ===
    panel = (events_df
             .groupby(['year', 'month', 'city'], as_index=False)['delta']
             .sum()
             .rename(columns={'delta': 'nums'})
             .sort_values(['year', 'month', 'city'])
             .reset_index(drop=True))

    print(panel.shape)
    return panel


if __name__ == '__main__':
    data_dir = Path("/Users/gaoxu/resources/招聘数据最终版")
    # 遍历所有 CSV 文件
    panels = []
    for file in sorted(data_dir.glob("*.csv")):
        print(f"▶️ 正在处理：{file.name}")
        current_panel = yearly_employment(str(file))
        panels.append(current_panel)

    # 直接纵向合并即可（各文件年份不同，不会冲突）
    final_panel = pd.concat(panels, ignore_index=True)

    # 可选：统一类型，排序一下更清爽
    final_panel['year'] = final_panel['year'].astype('Int64')
    final_panel['month'] = final_panel['month'].astype('Int64')
    final_panel = final_panel.sort_values(['year', 'month', 'city']).reset_index(drop=True)

    # 导出
    final_panel.to_csv("employment_monthly_panel2.csv", index=False, encoding="utf-8")
    print(final_panel.shape)
    print(f"✅ 已整合完成，共 {len(final_panel):,} 行 ")
