# AI 数据分析 Agent

一个面向非专业数据分析用户的 AI 数据分析助手。用户上传 CSV 或 Excel 文件后，可以通过自然语言提出分析问题，系统结合数据处理工具与 Agent 工作流，完成基础统计、分组聚合、分类排名等分析任务，并返回分析结果。

本项目是一个 AI 产品经理实践项目，重点探索如何将自然语言交互、数据分析工具和 Agent 工作流结合起来，降低业务用户进行数据分析的使用门槛。


## 核心功能

- **文件上传：** 支持 CSV 和 Excel 数据文件。
- **数据概览：** 查看数据行数、字段、数据类型、缺失值及重复数据等基本信息。
- **基础统计：** 计算常用统计指标。
- **分组聚合：** 按指定字段进行分组和汇总。
- **分类排名：** 对不同类别的指标进行排序。
- **自然语言分析：** 通过文字提出分析问题，由 Agent 工作流组织任务执行。
- **结果可视化：** 根据分析任务生成相应图表（以当前实现为准）。

## 技术方案

| 模块 | 技术或方案 | 作用 |
| --- | --- | --- |
| 前端交互 | Streamlit | 提供文件上传、问题输入和结果展示界面 |
| 数据处理 | Python、Pandas | 读取数据并执行统计与聚合计算 |
| 文件读取 | CSV、Excel | 支持结构化表格数据输入 |
| Agent 工作流 | Python 工作流与节点 | 组织分析计划、工具执行和结果整理 |
| 分析工具 | 自定义 Python 函数 | 执行统计、分组聚合、分类排名等操作 |
| 图表生成 | 项目中的图表生成模块 | 将部分分析结果转换为图表 |



## 项目结构

以下为项目的主要模块示意，实际文件名和目录以仓库当前版本为准。

```text
ai-data-analysis-agent/
├── agent/
│   └── workflow.py
├── services/
│   └── analysis_service.py
├── tools/
│   ├── data_loader.py
│   └── 数据分析相关工具
├── app.py
└── README.md
```

主要模块说明：

- `agent/`：负责组织 Agent 工作流程及任务执行。
- `services/`：封装分析服务的调用逻辑。
- `tools/`：提供数据读取、统计、分组聚合、排名等可复用工具。
- 应用入口文件：负责 Streamlit 界面和用户交互。

## 运行方式

### 环境准备

建议使用 Python 虚拟环境，并安装项目所需依赖。

```bash
python -m venv .venv
```

Windows PowerShell 激活虚拟环境：

```powershell
.venv\Scripts\Activate.ps1
```

如果仓库中提供了 `requirements.txt`，执行：

```bash
pip install -r requirements.txt
```

如果没有依赖文件，需要根据项目实际使用的库安装相应依赖。

### 启动应用

在项目根目录运行 Streamlit：

```bash
streamlit run app.py
```

如果实际入口文件不是 `app.py`，请替换为仓库中对应的文件名。

启动后，按照页面提示上传 CSV 或 Excel 文件，输入分析问题并查看结果。


---

**技术方向：** Python、Streamlit、Pandas、AI Agent、Workflow  
