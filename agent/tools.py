import json
import pandas as pd

from langchain_core.tools import tool

from tools.data_analyzer import (
    calculate_statistics,
    group_and_aggregate,
    rank_categories,
)


def create_analysis_tools(df: pd.DataFrame):
    """为当前上传的数据创建可调用工具。"""

    @tool
    def get_data_summary() -> str:
        """查看数据的行数、字段名、数据类型和缺失值情况。"""
        result = {
            "行数": len(df),
            "字段": [
                {"名称": str(col), "类型": str(df[col].dtype)}
                for col in df.columns
            ],
            "缺失值": {
                str(col): int(count)
                for col, count in df.isna().sum().items()
                if count > 0
            },
        }
        return json.dumps(result, ensure_ascii=False)

    @tool
    def calculate_column_statistics(column: str) -> str:
        """计算指定数值字段的总和、平均值、中位数、最小值和最大值。"""
        result = calculate_statistics(df, column)
        return json.dumps(result, ensure_ascii=False)


    @tool
    def summarize_by_group(
        group_column: str,
        value_column: str,
        agg: str = "sum",
        ascending: bool = False,
    ) -> str:
        """按类别分组统计数值。ascending=True 表示升序，False 表示降序。"""
    
        result = group_and_aggregate(
            df,
            group_column,
            value_column,
            agg=agg,
            ascending=ascending,
        )
    
        return result.to_json(
            orient="records",
            force_ascii=False
        )


    @tool
    def rank_by_category(
        category_column: str,
        value_column: str,
        top_n: int = 10,
    ) -> str:
        """按指定数值汇总类别排名，返回前 top_n 名。"""
        result = rank_categories(
            df, category_column, value_column, top_n=top_n
        )
        return result.to_json(
            orient="records", force_ascii=False
        )

    return [
        get_data_summary,
        calculate_column_statistics,
        summarize_by_group,
        rank_by_category,
    ]
