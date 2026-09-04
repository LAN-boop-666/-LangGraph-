"""State定义"""

from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages

class ResearchState(TypedDict):
  """研究助手全局状态"""

  messages: Annotated[list, add_messages] #消息历史

  #研究过程
  question: str #原始问题
  question_type: str #问题类型 simple/research/report
  search_results: str #搜索结果
  knowledge_results: str #知识库检索结果
  research_notes: str #研究笔记
  analysis: str #分析结果
  report: str #最终报告

  #控制
  itration: int #当前迭代次数
  review_passed: bool #是否通过审核
  review_feedback: str #审核反馈
  next_agent: str #下一个智能体
