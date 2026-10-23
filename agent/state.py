from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    # 用户提出的分析问题
    user_question: str

    # 上传的数据
    dataframe: Any

    # 数据概览
    data_summary: dict

    # Agent 制定的分析计划
    analysis_plan: list

    # 工具执行结果
    tool_results: list

    # 最终回答
    final_answer: str

    # 当前执行次数
    iteration_count: int

    # 执行过程中产生的错误
    error: str
