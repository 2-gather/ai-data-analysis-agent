
import pandas as pd

from tools.data_analyzer import (
    calculate_statistics,
    group_and_aggregate,
    rank_categories,
    analyze_trend,
)

df = pd.DataFrame({
    "日期": [
        "2026-01-01",
        "2026-01-15",
        "2026-02-01",
        "2026-02-10",
    ],
    "地区": ["华东", "华南", "华东", "华南"],
    "产品": ["A", "B", "A", "B"],
    "销售额": [100, 200, 300, 100],
})

print("=== 基础统计 ===")
print(calculate_statistics(df, "销售额"))

print("\n=== 按地区汇总 ===")
print(group_and_aggregate(df, "地区", "销售额"))

print("\n=== 产品销售额排名 ===")
print(rank_categories(df, "产品", "销售额", top_n=10))

print("\n=== 月度销售趋势 ===")
print(analyze_trend(df, "日期", "销售额"))
