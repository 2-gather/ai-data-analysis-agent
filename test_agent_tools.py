
import pandas as pd
from agent.tools import create_analysis_tools

df = pd.DataFrame({
    "地区": ["华东", "华南", "华东", "华南"],
    "产品": ["A", "B", "A", "B"],
    "销售额": [100, 200, 300, 100],
})

tools = create_analysis_tools(df)

for item in tools:
    print(item.name)

print("\n=== 测试分组汇总工具 ===")
group_tool = next(
    item for item in tools
    if item.name == "summarize_by_group"
)

result = group_tool.invoke({
    "group_column": "地区",
    "value_column": "销售额",
    "agg": "sum",
})

print(result)
