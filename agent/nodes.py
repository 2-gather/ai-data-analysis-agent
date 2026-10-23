import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage,ToolMessage

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)


def plan_node(state):
    """理解用户问题，制定分析计划。"""
    question = state["user_question"]
    summary = state.get("data_summary", {})

    messages = [
        SystemMessage(content="""
你是一个严谨的数据分析助手。
根据用户问题和数据字段，制定简洁、可执行的分析计划。
只能使用实际存在的字段，不得编造数据。
如果问题无法通过当前数据回答，要明确说明原因。
只输出分析计划，不要直接编造分析结果。
"""),
        HumanMessage(content=f"""
用户问题：{question}

当前数据概况：
{json.dumps(summary, ensure_ascii=False, default=str)}

请给出分析计划。
"""),
    ]

    response = llm.invoke(messages)

    return {
        "analysis_plan": [response.content],
        "iteration_count": state.get("iteration_count", 0) + 1,
    }




def execute_node(state):
    """让 Agent 分轮调用工具，直到获得结果或达到轮数上限。"""
    from agent.tools import create_analysis_tools

    df = state["dataframe"]
    tools = create_analysis_tools(df)
    model_with_tools = llm.bind_tools(tools)

    tool_map = {item.name: item for item in tools}
    tool_results = []

    messages = [
        SystemMessage(content="""
你是一个严谨的数据分析 Agent，必须使用工具获得真实计算结果。

规则：
1. 严格遵循用户原始问题，不能把“最低”理解为“最高”，反之亦然。
2. “哪个地区”表示按地区分组；指标使用用户指定的字段。
3. 分组比较或排名必须执行 summarize_by_group 或 rank_by_category。
4. 数据概览工具只能查看数据结构，不能代替实际统计。
5. 如果只获得数据概览，但用户要求排名、汇总或计算，必须继续调用相应的分析工具。
6. 工具参数必须使用真实存在的字段名称。
7. 只有获得实际计算结果后，才能给出数值结论。
8. 如果工具失败或无法完成任务，要明确说明原因，不得编造结果。
"""),
        HumanMessage(content=f"""
用户原始问题：
{state["user_question"]}

分析计划：
{state.get("analysis_plan", [])}

请完成用户要求的分析，不要只查看数据概览。
"""),
    ]

    max_rounds = 3

    for round_index in range(max_rounds):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            if not tool_results:
                tool_results.append({
                    "tool": "未调用工具",
                    "result": "模型没有调用分析工具，未能验证计算结果。",
                })
            break

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool = tool_map.get(tool_name)

            if tool is None:
                result_text = f"未找到工具：{tool_name}"
            else:
                try:
                    result_text = tool.invoke(tool_call["args"])
                    if not isinstance(result_text, str):
                        import json
                        result_text = json.dumps(
                            result_text, ensure_ascii=False, default=str
                        )
                except Exception as e:
                    result_text = f"工具执行失败：{e}"

            tool_results.append({
                "tool": tool_name,
                "result": result_text,
            })

            # 将工具结果交回模型，支持下一轮继续分析
            messages.append(
                ToolMessage(
                    content=str(result_text),
                    tool_call_id=tool_call["id"],
                )
            )

    return {
        "tool_results": tool_results,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }



def answer_node(state):
    """根据实际工具结果生成最终回答。"""
    messages = [
        SystemMessage(content="""
你是一个严谨的数据分析助手。
根据实际工具执行结果回答用户问题。

要求：
1. 结论必须有工具结果支持。
2. 可以解释数据表现，但不能把相关性说成因果关系。
3. 如果工具执行失败或没有返回有效结果，明确说明。
4. 用简洁中文回答，优先给出关键数字和结论。
"""),
        HumanMessage(content=f"""
用户问题：
{state["user_question"]}

分析计划：
{state.get("analysis_plan", [])}

实际工具结果：
{json.dumps(state.get("tool_results", []), ensure_ascii=False, default=str)}

请给出最终分析结论。
"""),
    ]

    response = llm.invoke(messages)

    return {"final_answer": response.content}
