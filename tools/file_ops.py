"""文件操作工具"""

import os
from langchain_core.tools import tool

@tool
def save_report(filename: str, content: str)->str :
  """
  将报告保存为md文件
  filename: 文件名（不包含路径，保存到./data/reports/）
  content: 文件内容（md格式）
  """
  try:
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.join(current_script_dir,"data","reports")
    print(f"报告目录: {report_dir}")
    os.makedirs(report_dir,exist_ok=True) #确保目录存在
    filepath = os.path.join(report_dir,filename)
    if not filepath.endswith(".md"):
      filepath += ".md"
    with open(filepath,"w",encoding="utf-8") as f:
      f.write(content)
    return f"报告保存成功，保存路径为：{filepath}"
  except Exception as e:
    return f"报告保存失败：{str(e)}"

@tool
def list_reports()->str:
  """
  列出所有已保存的报告
  """
  report_dir = "./data/reports"
  if not os.path.exists(report_dir):
    return "暂无报告"
  files = os.listdir(report_dir)  #列出目录下所有的文件
  if not files:
    return "暂无报告"
  result = "已保存的报告：\n"
  for f in files:
    size = os.path.getsize(os.path.join(report_dir,f))
    result += f"- {f} ({size}字节)\n"
  return result

if __name__ == "__main__":
  result = save_report.invoke(
    {"filename": "test_report","content":"这是一个测试报告。"}
  )
  print(result)

  result = list_reports.invoke({})
  print(result)