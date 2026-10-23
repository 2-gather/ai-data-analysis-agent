import pandas as pd


def calculate_statistics(df, column):
    """计算指定数值字段的基础统计指标。"""
    if column not in df.columns:
        raise ValueError(f"不存在字段：{column}")

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    if values.empty:
        raise ValueError(f"字段“{column}”没有可用的数值。")

    return {
        "字段": column,
        "有效数据量": int(len(values)),
        "总和": float(values.sum()),
        "平均值": float(values.mean()),
        "中位数": float(values.median()),
        "最小值": float(values.min()),
        "最大值": float(values.max()),
    }



def group_and_aggregate(
    df,
    group_column,
    value_column,
    agg="sum",
    ascending=False
):
    """按指定字段分组汇总，并支持升序或降序排序。"""

    if group_column not in df.columns:
        raise ValueError(f"不存在分组字段：{group_column}")

    if value_column not in df.columns:
        raise ValueError(f"不存在数值字段：{value_column}")

    if agg not in ["sum", "mean", "count", "median", "max", "min"]:
        raise ValueError("暂不支持该统计方式。")

    data = df[[group_column, value_column]].copy()
    data[value_column] = pd.to_numeric(
        data[value_column], errors="coerce"
    )
    data = data.dropna(subset=[group_column, value_column])

    if data.empty:
        raise ValueError("没有可用于分组统计的有效数据。")

    result = (
        data.groupby(group_column, as_index=False)[value_column]
        .agg(agg)
        .sort_values(
            value_column,
            ascending=ascending
        )
        .reset_index(drop=True)
    )

    return result



def rank_categories(df, category_column, value_column, top_n=10):
    """按数值字段排名，返回前 N 个类别。"""
    if category_column not in df.columns:
        raise ValueError(f"不存在类别字段：{category_column}")

    if value_column not in df.columns:
        raise ValueError(f"不存在数值字段：{value_column}")

    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
        raise ValueError("top_n 必须是正整数。")

    data = df[[category_column, value_column]].copy()
    data[value_column] = pd.to_numeric(
        data[value_column], errors="coerce"
    )
    data = data.dropna(subset=[category_column, value_column])

    result = (
        data.groupby(category_column, as_index=False)[value_column]
        .sum()
        .sort_values(value_column, ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return result


def analyze_trend(df, date_column, value_column, frequency="ME"):
    """按时间汇总指标，生成趋势数据。"""
    if date_column not in df.columns:
        raise ValueError(f"不存在日期字段：{date_column}")

    if value_column not in df.columns:
        raise ValueError(f"不存在数值字段：{value_column}")

    if frequency not in ["D", "W", "ME", "MS", "QE", "YS"]:
        raise ValueError("暂不支持该时间频率。")

    data = df[[date_column, value_column]].copy()
    data[date_column] = pd.to_datetime(
        data[date_column], errors="coerce"
    )
    data[value_column] = pd.to_numeric(
        data[value_column], errors="coerce"
    )
    data = data.dropna(subset=[date_column, value_column])

    if data.empty:
        raise ValueError("没有可用于趋势分析的有效数据。")

    result = (
        data.set_index(date_column)[value_column]
        .resample(frequency)
        .sum()
        .dropna()
        .reset_index()
    )

    return result
