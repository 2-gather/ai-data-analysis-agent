
import plotly.express as px


def generate_chart(df, chart_type, x_column, y_column, title="数据分析图表"):
    """根据数据和指定类型生成图表。"""

    if x_column not in df.columns:
        raise ValueError(f"不存在字段：{x_column}")

    if y_column not in df.columns:
        raise ValueError(f"不存在字段：{y_column}")

    if chart_type == "bar":
        fig = px.bar(df, x=x_column, y=y_column, title=title)

    elif chart_type == "line":
        fig = px.line(df, x=x_column, y=y_column, title=title)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_column, y=y_column, title=title)

    elif chart_type == "pie":
        fig = px.pie(
            df,
            names=x_column,
            values=y_column,
            title=title
        )

    else:
        raise ValueError(
            "暂不支持该图表类型，请使用 bar、line、scatter 或 pie。"
        )

    fig.update_layout(
        template="plotly_white",
        xaxis_title=x_column,
        yaxis_title=y_column
    )

    return fig
