#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量合并百度指数月度 CSV → (year, month, city, searched) 面板
---------------------------------------------------------------
要求：
  1. 每个 CSV 只用到 3 列：关键词 | 日期 | PC+移动端
  2. 文件名格式：<城市名>-xxxx.csv   # 城市名取首段
  3. 输出按 (year, month, city) 聚合求和，列顺序固定

执行后生成：
  panel_2011_2023_month_city_searched.csv
"""

import os, glob
import pandas as pd

# ===== 1. 数据目录（改成你的绝对路径） ========================
DATA_DIR = r"/Users/gaoxu/resources/百度指数-所有城市-矩阵(2011-2023年度总和)-含日月年源数据/月度总和-源数据"
PATTERN = "*-月度总和.csv"

# 尝试的编码列表（常见中文编码）
ENCODINGS = ["utf-8-sig", "utf-8", "gbk", "gb18030"]


# ===== 2. 读取工具 ===========================================
def read_csv_fixed_cols(path):
    """只读取固定三列，尝试多种编码"""
    for enc in ENCODINGS:
        try:
            return pd.read_csv(
                path,
                encoding=enc,
                usecols=["关键词", "日期", "PC+移动端"]
            )
        except Exception:
            continue
    raise RuntimeError(f"读取失败（编码问题？）：{path}")


# ===== 3. 主流程 =============================================
panel_rows = []

for fp in sorted(glob.glob(os.path.join(DATA_DIR, PATTERN))):
    city = os.path.basename(fp).split("-")[0]  # 取文件名前缀作为城市
    df = read_csv_fixed_cols(fp)

    # 统一把“日期”转字符串 → 去掉非数字 → YYYYMMDD
    clean_dates = (
        df["日期"].astype(str)
        .str.replace(r"\D", "", regex=True)
    )

    # 取前 4 位年份、5~6 位月份
    years = clean_dates.str.slice(0, 4).astype(int)
    months = clean_dates.str.slice(4, 6).astype(int)

    # 写入行列表
    panel_rows.extend({
                          "year": y,
                          "month": m,
                          "city": city,
                          "searched": v
                      } for y, m, v in zip(years, months, df["PC+移动端"]))

# ===== 4. 合并 & 去重聚合 =====================================
panel = pd.DataFrame(panel_rows)

# 转数值、NaN→0，然后按 (year, month, city) 聚合求和
panel["searched"] = pd.to_numeric(panel["searched"], errors="coerce").fillna(0)
panel = (
    panel.groupby(["year", "month", "city"], as_index=False)["searched"]
    .sum()
)

# 固定列顺序 & 排序
panel = panel[["year", "month", "city", "searched"]] \
    .sort_values(["city", "year", "month"])

# ===== 5. 导出 ===============================================
panel.to_csv("panel_2011_2023_month_city_searched.csv",
             index=False, encoding="utf-8-sig")

print("✅ 完成！唯一组合行数：", panel.shape[0])
