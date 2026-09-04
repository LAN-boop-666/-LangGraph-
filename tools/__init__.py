from tools.search import search_web, search_arxiv
from tools.file_ops import list_reports, save_report
from tools.knowledge import search_knowledge_base

# 所有可用工具
ALL_TOOLS = [
    search_web,
    search_arxiv,
    list_reports,
    save_report,
    search_knowledge_base,
]