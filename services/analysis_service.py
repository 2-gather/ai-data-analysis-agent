import os
from agent.workflow import build_workflow


def is_ai_enabled():
    """读取 AI 开关，默认关闭。"""
    try:
        import streamlit as st

        value = st.secrets.get("AI_ENABLED", False)
    except Exception:
        value = os.getenv("AI_ENABLED", "false")

    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in ("true", "1", "yes", "on")


def run_analysis(df, question):
    """运行数据分析 Agent，返回分析计划、工具结果和最终结论。"""

    if df is None or df.empty:
        raise ValueError("没有可分析的数据，请先上传文件。")

    if not question or not question.strip():
        raise ValueError("请输入你想分析的问题。")

    # 关闭 AI 时，禁止进入 Agent 工作流
    if not is_ai_enabled():
        raise RuntimeError(
            "当前 Demo 处于展示模式，请联系管理员开放AI分析功能。"
        )

    # 整理数据概况，提供给 Agent 理解数据结构
    data_summary = {
        "行数": len(df),
        "字段": [
            {
                "名称": str(col),
                "类型": str(df[col].dtype),
            }
            for col in df.columns
        ],
        "缺失值": {
            str(col): int(count)
            for col, count in df.isna().sum().items()
            if count > 0
        },
    }

    # 创建并运行 LangGraph 工作流
    workflow = build_workflow()

    result = workflow.invoke({
        "user_question": question.strip(),
        "dataframe": df,
        "data_summary": data_summary,
        "analysis_plan": [],
        "tool_results": [],
        "final_answer": "",
        "iteration_count": 0,
        "error": "",
    })

    return {
        "analysis_plan": result.get("analysis_plan", []),
        "tool_results": result.get("tool_results", []),
        "final_answer": result.get("final_answer", ""),
    }
