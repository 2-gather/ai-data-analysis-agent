import pandas as pd


def load_data(uploaded_file):
    """读取用户上传的 CSV 或 Excel 文件。"""
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="gb18030")

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    else:
        raise ValueError("当前仅支持 CSV / XLSX 文件。")

    if df.empty or len(df.columns) == 0:
        raise ValueError("当前文件没有可分析的数据。")

    return df


def get_data_summary(df):
    """生成数据规模、字段类型和数据质量概览。"""

    # 数据规模
    row_count = len(df)
    column_count = len(df.columns)

    # 字段信息
    field_info = pd.DataFrame({
        "字段名称": df.columns.astype(str),
        "数据类型": [str(dtype) for dtype in df.dtypes],
        "非空值数量": df.notna().sum().values,
        "缺失值数量": df.isna().sum().values,
    })

    # 重复记录数量
    duplicate_count = int(df.duplicated().sum())

    # 各字段缺失值数量
    missing_info = df.isna().sum()
    missing_info = missing_info[missing_info > 0]

    return {
        "row_count": row_count,
        "column_count": column_count,
        "field_info": field_info,
        "duplicate_count": duplicate_count,
        "missing_info": missing_info,
    }
