"""
  前置操作：
      1、普通用户登录（类级别）
      2、管理员登录（类级别）
      3、添加项目（类级别）
      4、审核项目（类级别）

   用例前置操作的封装优化：
      1、把多个用例要使用的一些前置步骤封装到一个类中
      2、需要使用这些前置步骤的测试类，直接去继承（多继承）封装好的前置步骤方法
      3、在类级别的前和用例级别的前置中，调用对应的前置方法即

  用例方法：
      1、准备数据
      2、发送请求
      3、断言

      #数据校验
           用户表： 用户的余额投资前后会变化
                投资前-投资后 ==投资的金额

           流水记录表： 投资成功会新增一条流水记录
                 投资后用户流水记录数量 - 投资前用户的记录数量 ==1

           投资表: 投资成功会新增一条投资记录
                 投资后用户的记录数量-投资前用户的记录数最==1

       ------扩展投资后（可投金额为0）满标的情况，会生成回款计划---------自行去研究
                1、先把项目的投资记录id都查询出来
                2、遍历投资记录id
                3、根据每个投资记录的id去查询是否生成回款计划表:

"""
import os
import  unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.Handle_Excel import HandleExcel
from common.handle_config import conf
from common.handler_log import mylog
from common.handler_path import DATA_DIR
from testcases.fixture import BaseTest
from common.tools import Test
from  common.handle_pymysql import HandleDB



# self: 是实列方法的第一个参数，代表的是实列对象的本身
# cls:  是类方法的第一个参数，代表的是类的本身


@ddt
class TestInvest(unittest.TestCase,BaseTest):
    excel=HandleExcel(os.path.join(DATA_DIR,"aa.xlsx"),"invest")
    case=excel.read_data()
    db=HandleDB()

    #调用封装的类前置
    @classmethod
    def setUpClass(cls) -> None:
         #普通用户登录
         cls.user_login()
         #管理员登录
         cls.admin_loan()
         #普通用户添加项目
         cls.add_project()
         #审核
         cls.audit()



    @list_data(case)
    def test_invest(self,item):
        #第一步：准备数据
        url=conf.get("env","url")+item["url"]
        item["data"]=Test.replace_data(item["data"],TestInvest)
        params=eval(item["data"])
        expected=eval(item["expected"])
        method=item["method"]
        #----------------投资前查询数据库------------
        # 查用户表的sql
        sql1 = "SELECT leave_amount FROM member WHERE id='{}'".format(self.member_id)
        #查投资记录的sql
        sql2 = "SELECT id FROM invest WHERE member_id='{}'".format(self.member_id)
        # 查流水记录的sql
        sql3 = "SELECT id FROM financelog WHERE pay_member_id='{}'".format(self.member_id)
        # 判断是否含有check_sql，如果有就执行
        if item["check_sql" ]:
                s_amount = self.db.find_one(sql1)[0]
                s_invest = self.db.find_count(sql2)
                s_financelog = self.db.find_count(sql3)
        #第二步：发生请求
        response=requests.request(method=method,json=params,url=url,headers=self.headers)
        res=response.json()
        print("预期结果"+str(expected))
        print("实际结果"+str(res))
        #----------------投资后查询数据库------------
        if item["check_sql"]:
            e_amount = self.db.find_one(sql1)[0]
            e_invest = self.db.find_count(sql2)
            e_financelog = self.db.find_count(sql3)

        # 第三步：断言
        try:
            self.assertEqual(expected['code'], res['code'])
            #断言实际结果中的msg是否包含预期结果msq的结果内容，使用“assertIn”
            self.assertIn(expected['msg'], res['msg'])
            if item["check_sql"]:
                #断言用户余额
                self.assertEqual(params["amount"],float(s_amount-e_amount))
                #断言投资记录
                self.assertEqual(1,e_invest-s_invest)
                #断言流水记录
                self.assertEqual(1,e_financelog-s_financelog)

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