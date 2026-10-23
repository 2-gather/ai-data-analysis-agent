from services.analysis_service import run_analysis
import streamlit as st
import pandas as pd

from tools.data_loader import load_data, get_data_summary
from tools.data_analyzer import (
    calculate_statistics,
    group_and_aggregate,
    rank_categories,
    analyze_trend,
)
from tools.chart_generator import generate_chart


st.set_page_config(
    page_title="AI 数据分析 Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI 数据分析 Agent")
st.caption("上传数据，完成统计分析、分组汇总与可视化。")

uploaded_file = st.file_uploader(
    "上传 CSV 或 Excel 文件",
    type=["csv", "xlsx"],
)

if uploaded_file is None:
    st.info("请先上传 CSV 或 XLSX 文件。")
    st.stop()

# 点击按钮后分析
if st.button("🚀 开始分析", type="primary", use_container_width=True):
    st.session_state["analysis_started"] = True

# 尚未开始分析，就停留在首页
if not st.session_state.get("analysis_started", False):
    st.info(f"已上传文件：{uploaded_file.name}，点击「开始分析」继续。")
    st.stop()

try:
    df = load_data(uploaded_file)
    summary = get_data_summary(df)
except Exception as e:
    st.error(f"文件读取失败：{e}")
    st.stop()
except Exception as e:
    st.error(f"文件读取失败：{e}")
    st.stop()


# 一、数据概览
st.header("一、数据概览")

c1, c2, c3, c4 = st.columns(4)
c1.metric("数据行数", len(df))
c2.metric("字段数量", len(df.columns))
c3.metric("重复行数", summary["duplicate_count"])
c4.metric("缺失单元格数", int(df.isna().sum().sum()))

with st.expander("查看数据预览", expanded=True):
    st.dataframe(df.head(20), use_container_width=True)

with st.expander("查看字段信息"):
    st.dataframe(summary["field_info"], use_container_width=True)

if not summary["missing_info"].empty:
    with st.expander("查看缺失值分布"):
        st.dataframe(
            summary["missing_info"].rename("缺失数量").to_frame(),
            use_container_width=True,
        )


# 二、基础统计
st.header("二、基础统计")

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if numeric_columns:
    stat_column = st.selectbox(
        "选择需要统计的数值字段",
        numeric_columns,
        key="stat_column",
    )

    if st.button("计算统计指标"):
        try:
            result = calculate_statistics(df, stat_column)
            st.dataframe(
                pd.DataFrame([result]),
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"统计失败：{e}")
else:
    st.warning("没有检测到数值类型字段，暂时无法进行基础数值统计。")


# 三、分组汇总与排名
st.header("三、分组汇总与排名")

all_columns = df.columns.astype(str).tolist()

col1, col2 = st.columns(2)

with col1:
    group_column = st.selectbox(
        "分组字段",
        all_columns,
        key="group_column",
    )

with col2:
    value_candidates = numeric_columns or all_columns
    value_column = st.selectbox(
        "统计字段",
        value_candidates,
        key="group_value_column",
    )

agg_method = st.selectbox(
    "汇总方式",
    ["sum", "mean", "count", "median", "max", "min"],
    format_func=lambda x: {
        "sum": "求和",
        "mean": "平均值",
        "count": "计数",
        "median": "中位数",
        "max": "最大值",
        "min": "最小值",
    }[x],
)

if st.button("执行分组汇总"):
    try:
        result = group_and_aggregate(
            df, group_column, value_column, agg=agg_method
        )
        st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(f"分组汇总失败：{e}")

if numeric_columns:
    rank_value = st.selectbox(
        "排名指标",
        numeric_columns,
        key="rank_value",
    )
    rank_category = st.selectbox(
        "排名类别",
        all_columns,
        key="rank_category",
    )
    top_n = st.number_input(
        "显示前 N 名",
        min_value=1,
        max_value=100,
        value=10,
    )

    if st.button("生成排名"):
        try:
            result = rank_categories(
                df,
                rank_category,
                rank_value,
                top_n=int(top_n),
            )
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"排名生成失败：{e}")


# 四、图表生成
st.header("四、图表生成")

chart_type = st.selectbox(
    "图表类型",
    ["bar", "line", "scatter", "pie"],
    format_func=lambda x: {
        "bar": "柱状图",
        "line": "折线图",
        "scatter": "散点图",
        "pie": "饼图",
    }[x],
)

chart_x = st.selectbox(
    "横轴 / 类别字段",
    all_columns,
    key="chart_x",
)

chart_y = st.selectbox(
    "纵轴 / 数值字段",
    numeric_columns or all_columns,
    key="chart_y",
)

chart_title = st.text_input(
    "图表标题",
    value="数据分析图表",
)

if st.button("生成图表"):
    try:
        fig = generate_chart(
            df=df,
            chart_type=chart_type,
            x_column=chart_x,
            y_column=chart_y,
            title=chart_title,
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"图表生成失败：{e}")


# 五、时间趋势分析
st.header("五、时间趋势分析")

date_candidates = [
    col for col in all_columns
    if (
        pd.api.types.is_datetime64_any_dtype(df[col])
        or any(word in str(col).lower()
               for word in ["日期", "时间", "date", "time"])
    )
]

if date_candidates and numeric_columns:
    trend_date = st.selectbox(
        "时间字段",
        date_candidates,
        key="trend_date",
    )
    trend_value = st.selectbox(
        "趋势指标",
        numeric_columns,
        key="trend_value",
    )
    frequency_label = st.selectbox(
        "统计频率",
        ["按日", "按周", "按月"],
    )
    frequency = {
        "按日": "D",
        "按周": "W",
        "按月": "ME",
    }[frequency_label]

    if st.button("分析变化趋势"):
        try:
            trend_df = analyze_trend(
                df, trend_date, trend_value, frequency=frequency
            )
            st.dataframe(trend_df, use_container_width=True)

            fig = generate_chart(
                trend_df,
                "line",
                trend_df.columns[0],
                trend_df.columns[1],
                title=f"{trend_value}趋势分析",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"趋势分析失败：{e}")
else:
    st.info("未识别到合适的时间字段或数值字段，暂时跳过趋势分析。")



# 六、AI 智能分析
st.divider()
st.header("六、AI 智能分析")
st.caption("直接用自然语言提问，由 Agent 自动选择数据分析工具。")

question = st.text_input(
    "你想分析什么？",
    placeholder="例如：哪个地区的销售额最高？",
    key="agent_question",
)

if st.button("开始智能分析", type="primary"):
    if not question.strip():
        st.warning("请先输入分析问题。")
    else:
        with st.spinner("Agent 正在分析，请稍候..."):
            try:
                result = run_analysis(df, question)

                st.subheader("分析计划")
                for plan in result["analysis_plan"]:
                    st.markdown(plan)

                st.subheader("工具执行记录")
                for item in result["tool_results"]:
                    with st.expander(f"工具：{item['tool']}"):
                        st.write(item["result"])

                st.subheader("分析结论")
                st.markdown(result["final_answer"])

            except Exception as e:
                st.error(f"分析失败：{e}")

st.caption("AI 数据分析 Agent｜MVP 测试版")
