"""
充值的前提：登录-->提取token
unittest:
     用例级别的前置：setUp
     测试类级别的前置：setUpClass
         1、提取token，保存为类属性
         2、提取用户id，保存为类属性
    充值测试方法：
         1、动态的替换参数中的用户id(字符串的replace中的参数要是字符串类型)

注册类的优化：
      1、手机号码动态生成，替换到用例参数中

"""
import os
import unittest
import requests
from jsonpath import jsonpath
from common.Handle_Excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_config import conf
from unittestreport import ddt,list_data
from common.handler_log import mylog
from common.handle_pymysql import HandleDB
from common.tools import Test


@ddt
class TestRecharge(unittest.TestCase):
    excel=HandleExcel(os.path.join(DATA_DIR,"aa.xlsx"),"recharge")
    cases=excel.read_data()
    db = HandleDB()


    """ 用例类的前置方法，登录提取token"""
    @classmethod
    def setUpClass(cls):
        #1、请求登录接口，进行登录
        url=conf.get("env","url")+"/member/login"
        params={
               "mobile_phone":conf.get("test","mobile"),
                "pwd":conf.get("test","pwd")
        }
        headers=eval(conf.get("env","headers"))
        response=requests.post(url=url,json=params,headers=headers)
        res=response.json()
        print(res)
        #2、登录成功之后再去提取token值("$":取根节点，"..":就是不管位置，选择所有符合条件的条件,"[0]":取值)
        token=jsonpath(res,"$..token")[0]
        #将token添加到请求头
        headers["Authorization"]="Bearer "+token
        #保存含有token的请求头为类属性
        cls.headers=headers
        #3、提取用户的id给充值接口使用
        cls.member_id=jsonpath(res,"$..id")[0]

    @list_data(cases)
    def test_recharge(self,item):
         #第一步:准备数据
         url=conf.get("env","url")+item["url"]
         """*****************动态替换参数**********************"""
         #动态处理需要进行替换的参数
         # item["data"]=item["data"].replace("#member_id#",str(self.member_id))

         #todo 使用封装方法来替换数据
         item["data"] =Test.replace_data(item["data"],TestRecharge)

         params=eval(item["data"])
         # print(params)
         #*****************************************************
         #获取预期值
         expected=eval(item["expected"])
         method=item["method"].lower()

         #todo****************充值之前的数据查询******************
         sql='select leave_amount from member where mobile_phone="{}"'.format(conf.get("test","mobile"))
         start_amount=self.db.find_one(sql)[0]
         print("充值之前"+str(start_amount))

         #第二步：发送请求，获取接口返回的实际结果
         response=requests.request(method=method,url=url,json=params,headers=self.headers)
         res =response.json()

         # todo****************充值之后的数据查询******************
         end_amount = self.db.find_one(sql)[0]
         print("充值之后"+str(end_amount))

         # print("预期结果"+str(expected))
         # print("实际结果"+str(res))
         #断言
         try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])

             #todo*******************校验数据库中用户余额的变化是否等于充值的金额**************************
            if res["msg"]=="OK":
                #充值成功,用户余额的变化为充值金额
                self.assertEqual(int(end_amount-start_amount),int(params["amount"]))
            else:
                #充值失败,用户余额的变化为0
                self.assertEqual(float(end_amount-start_amount),0)

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
