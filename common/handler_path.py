"""
此模块专门用例处理项目中的绝对路径
os.path.abspath(__file__)：获取当前文件目录所在位置
os.path.dirname:每嵌套一次就返回一次上一级目录

"""
import  os

#项目的根目录的绝对路径
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#用例数据所在目录：
DATA_DIR=os.path.join(BASE_DIR,"datas")

#配置文件的根目录
CONF_DIR=os.path.join(BASE_DIR,"confs")

#日志文件的根目录
LOG_DIR=os.path.join(BASE_DIR,"logs")

#报告所在的路径
REPORT_DIR=os.path.join(BASE_DIR,"reports")

#用例模块所在的目录
CASES_DIR=os.path.join(BASE_DIR,"testcases")
# print(DATA_DIR)