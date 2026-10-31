# LangGraph 智能研究助手

一个基于 LangGraph 的多智能体研究助手。它会先判断问题类型，再按需调用网络搜索、arXiv、本地知识库和文件工具，最后由研究、分析、写作节点生成结构化报告，并通过质量审查节点进行循环修正。

## 能做什么

- **问题路由**：区分闲聊/常识、一般研究问题和深度报告问题。
- **网络检索**：通过 Tavily 搜索最新公开信息。
- **学术检索**：通过 arXiv API 查询论文。
- **本地 RAG**：读取 `data/knowledge/` 下的 Markdown 文档，切分后写入 Chroma，并按问题检索。
- **多智能体协作**：researcher 负责整理资料，analyst 负责分析，writer 负责生成报告。
- **质量审查与记忆**：报告不通过时回到研究节点重做；LangGraph 使用 MemorySaver 保存线程状态。
- **报告文件工具**：可以列出和保存 Markdown 报告。

## 工作流程

```text
用户问题
   |
classify
   |-- simple --> simple_answer --> END
   |
research/report
   |
tool_calling --> tool_executor --> collect
   |                             
researcher --> analyst --> writer --> review
                                      |-- PASS --> END
                                      |-- REVISE --> researcher（最多 3 轮）
```

## 环境要求

- Python 3.10+
- 可访问的 OpenAI 兼容大模型接口
- 可选：Tavily API（网络搜索）
- 可选：Embedding 兼容接口（本地知识库 RAG）

## 安装

PowerShell：

```powershell
git clone https://github.com/LAN-boop-666/-LangGraph-.git
cd -LangGraph-

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirement.txt
```

如果 PowerShell 允许激活虚拟环境，也可以执行：

```powershell
.\.venv\Scripts\Activate.ps1
```

## 配置模型和工具

在仓库根目录新建 `.env`。只填写自己的配置，不要把密钥提交到 Git：

```dotenv
# 必填：OpenAI 兼容聊天模型
LLM_API_KEY=你的模型密钥
LLM_BASE_URL=https://api-inference.modelscope.cn/v1/
LLM_MODEL_ID=Qwen/Qwen3.5-35B-A3B
LLM_TIMEOUT=60
LLM_TEMPERATURE=0

# 使用 Tavily 网络搜索时填写
TAVILY_API_KEY=你的Tavily密钥

# 使用本地 RAG 时填写
EMBED_MODEL_NAME=你的Embedding模型名
EMBED_API_KEY=你的Embedding密钥
EMBED_BASE_URL=你的Embedding接口地址
```

`LLM_BASE_URL` 和 `EMBED_BASE_URL` 都要求服务提供 OpenAI 兼容接口。不要在 README、日志或提交记录中填写真实密钥。

## 最小运行示例

项目没有强制绑定某个 Web 服务，最简单的方式是从仓库根目录创建一个临时文件 `run_demo.py`：

```python
from langchain_core.messages import HumanMessage
from graph import build_graph

graph = build_graph()
result = graph.invoke(
    {"messages": [HumanMessage(content="请研究 LangGraph 在多智能体系统中的作用，并给出结构化报告。")]},
    {"configurable": {"thread_id": "demo-001"}},
)

print(result.get("report", ""))
```

运行：

```powershell
.\.venv\Scripts\python.exe .\run_demo.py
```

说明：

1. `build_graph()` 创建并编译 LangGraph 工作流。
2. `messages` 中放入用户问题，图会自动补充 `question` 和问题类型。
3. `thread_id` 用于 MemorySaver 识别对话线程；同一个线程可以继续传入后续问题。
4. 深度研究任务通常会调用搜索工具并生成 `result["report"]`；简单问题则主要查看 `result["messages"]`。
5. 这是一次真实模型调用，需要有效的 `LLM_API_KEY`、模型名和接口地址。

## 启用本地知识库 RAG

知识库文件放在 `data/knowledge/`。首次构建向量库：

```powershell
.\.venv\Scripts\python.exe .\tools\knowledge.py
```

该命令会读取 Markdown、调用 Embedding 接口并生成 `data/vector_store/`。之后研究助手会自动复用已有向量库；如果向量库不存在，知识库工具会尝试重新构建。

RAG 需要同时配置 `EMBED_MODEL_NAME`、`EMBED_API_KEY` 和 `EMBED_BASE_URL`。只使用普通问答或网络搜索时，可以暂不配置这三项。

## 直接测试单个工具

```powershell
# 测试 Tavily 搜索，要求已配置 TAVILY_API_KEY
.\.venv\Scripts\python.exe .\tools\search.py

# 测试文件工具和报告目录
.\.venv\Scripts\python.exe .\tools\file_ops.py
```

## 目录结构

```text
agent/
  researcher.py       研究节点
  analyst.py          分析节点
  writer.py           写作节点和报告结构
tools/
  search.py           Tavily、arXiv 搜索
  knowledge.py        Embedding、Chroma、RAG
  file_ops.py         报告保存和列表
data/knowledge/       本地 Markdown 知识库
data/vector_store/    首次 RAG 构建后生成，已被 Git 忽略
graph.py              LangGraph 图和路由
state.py              共享状态定义
requirement.txt       Python 依赖
readme.md             设计说明
```

## 常见问题

- **提示未配置 `LLM_API_KEY`**：检查 `.env` 是否位于仓库根目录，变量名是否完全一致。
- **网络搜索返回未配置密钥**：填写 `TAVILY_API_KEY`；不使用网络搜索时可忽略。
- **RAG 提示缺少 `EMBED_*`**：填写三个 Embedding 配置后重新运行 `tools/knowledge.py`。
- **导入失败**：确认命令是在仓库根目录执行，并使用 `.venv\Scripts\python.exe`。
- **报告为空**：先查看 `result["messages"]` 和终端日志，确认模型接口是否正常返回。

## 依赖

主要依赖见 [requirement.txt](requirement.txt)：

- LangGraph
- LangChain Core / Community / OpenAI
- Chroma
- Tavily
- python-dotenv
- requests / httpx
