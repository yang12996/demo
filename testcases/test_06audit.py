"""
审核接口： 管理员去审核

审核的前置条件：
   1、管理员登录（类级别的前置）

   2、普通用户的角色添加项目
        1）、普通用户登录（类级别的前置）
        2）、创建一个项目（用例级别的前置）
"""
import unittest
import os
import  requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_config import conf
from common.handler_log import mylog
from common.handler_path import DATA_DIR
from common.Handle_Excel import HandleExcel
from common.tools import Test

@ddt
class TestAudit(unittest.TestCase):
    excel=HandleExcel(os.path.join(DATA_DIR,"aa.xlsx"),"audit")
    case=excel.read_data()

    # 使用类前置
    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get("env", "url") + "/member/login"
    #*******************管理员登录*****************************
        # 1、准备登录数据
        url = conf.get("env", "url") + "/member/login"
        params = {
            "mobile_phone": conf.get("test", "admin_mobile"),
            "pwd": conf.get("test", "admin_pwd")
        }
        headers = eval(conf.get("env", "headers"))
        # 2、请求登录接口
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        # 3、登录成功之后再去提取token值("$":取根节点，"..":就是不管位置，选择所有符合条件的条件,"[0]":取值)
        admin_token = jsonpath(res, "$..token")[0]
        # 将token添加到请求头
        headers["Authorization"] = "Bearer " + admin_token
        # 保存含有token的请求头为类属性
        cls.admin_headers = headers
        # 4、提取用户的id给充值接口使用
        cls.admin_member_id = jsonpath(res, "$..id")[0]

    #*******************普通登录*****************************
        # 1、准备登录数据
        params = {
            "mobile_phone": conf.get("test", "mobile"),
            "pwd": conf.get("test", "pwd")
        }
        headers = eval(conf.get("env", "headers"))
        # 2、请求登录接口
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        # 3、登录成功之后再去提取token值("$":取根节点，"..":就是不管位置，选择所有符合条件的条件,"[0]":取值)
        token = jsonpath(res, "$..token")[0]
        # 将token添加到请求头
        headers["Authorization"] = "Bearer " + token
        # 保存含有token的请求头为类属性
        cls.headers = headers
        # 4、提取用户的id给充值接口使用
        cls.member_id = jsonpath(res, "$..id")[0]

    # 使用用例前置
    def setUp(self) -> None:
        """用例级别的前置:添加项目"""
        #第一步：准备数据
        url = conf.get("env", "url") + "/loan/add"
        params={"member_id":self.member_id,
                "title":"借款",
                "amount":2000,
                "loan_rate":12.0,
                "loan_term":3,
                "loan_date_type":1,
                "bidding_days":5}
        #第二步：请求添加项目的接口
        response=requests.request(method="post",url=url,json=params,headers=self.headers)
        res=response.json()
        #第三步：提取项目的id,保存为类属性
        TestAudit.loan_id = jsonpath(res, "$..id")[0]


    @list_data(case)
    def test_audit(self,item):
          #第一步：准备数据
          url=conf.get("env","url")+item["url"]
          item["data"]=Test.replace_data(item["data"],TestAudit)
          params=eval(item["data"])
          method=item["method"]
          expected=eval(item["expected"])
          #第二步：请求接口
          response=requests.request(method=method,url=url,json=params,headers=self.admin_headers)
          res=response.json()

          #todo 判断是否审核通过的用例，并且审核成功，如果成功则保存项目id为审核通过的项目id
          if res["msg"]=="OK" and item["title"]=="审核通过":
              TestAudit.pass_loan_id=params["loan_id"]

          # 第三步：断言
          try:
              self.assertEqual(expected['code'], res['code'])
              self.assertEqual(expected['msg'], res['msg'])

          except AssertionError as e:
              mylog.error("用例--【{}】----执行失败".format(item["title"]))
              mylog.error(e)
              # 记录详细的错误信息到日志用exception
              # mylog.exception(e)
              raise e
          else:
              # self.excel.write_data(row=row,column=5,value="通过")
              # 记录运行成功日志
              mylog.info("用例--【{}】----执行成功".format(item["title"]))