
import pandas as pd
from tools.chart_generator import generate_chart

df = pd.DataFrame({
    "产品": ["A", "B", "C"],
    "销售额": [400, 300, 200]
})

fig = generate_chart(
    df=df,
    chart_type="bar",
    x_column="产品",
    y_column="销售额",
    title="产品销售额对比"
)

fig.write_html("test_chart.html", include_plotlyjs=True)
print("图表已保存到项目根目录的 test_chart.html")
