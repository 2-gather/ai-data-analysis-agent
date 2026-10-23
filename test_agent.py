import pandas as pd
from services.analysis_service import run_analysis

df = pd.DataFrame({
    "地区": ["华东", "华南", "华东", "华南"],
    "产品": ["A", "B", "A", "B"],
    "销售额": [100, 200, 300, 100],
})

question = "哪个地区的销售额最高？请展示各地区销售额并说明结果。"

result = run_analysis(df, question)

print("\n=== 分析计划 ===")
print(result["analysis_plan"])

print("\n=== 工具执行结果 ===")
for item in result["tool_results"]:
    print("工具：", item["tool"])
    print("结果：", item["result"])

print("\n=== 最终结论 ===")
print(result["final_answer"])
