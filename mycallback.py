"""自定义回调：各种Agent LLM执行过程"""

from langchain_core.callbacks import BaseCallbackHandler
import logging

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  force=True,
)
logger = logging.getLogger("researcher_node")

class ResearchCallbackHandler(BaseCallbackHandler):
  """研究助手项目的llm回调处理函数"""
  def on_llm_start(self, run_id: str, llm_call: dict):
