import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handler_path import DATA_DIR
from common.Handle_Excel import HandleExcel
from common.handle_config import conf
from common.tools import Test
from common.handler_log import mylog
from common.handle_pymysql import HandleDB

"""
    添加项目:需要登录（使用类级别前置获取token,member_id）
"""

@ddt
class TsetAdd(unittest.TestCase):
    excel =HandleExcel(os.path.join(DATA_DIR,"aa.xlsx"),"add")
    cases=excel.read_data()
    db=HandleDB()
    @classmethod
    def setUpClass(cls) -> None:
        """前置登录"""
        # 1、准备登录数据
        url=conf.get("env","url")+"/member/login"
        params={
            "mobile_phone":conf.get("test", "mobile"),
             "pwd":conf.get("test", "pwd")
        }
        headers=eval(conf.get("env","headers"))
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

    @list_data(cases)
    def test_add(self,itme):
        #第一步:准备数据
        url=conf.get("env","url")+itme["url"]
        #使用类属性值替换数据
        itme["data"]=Test.replace_data(itme["data"],TsetAdd)
        #获取参数
        params=eval(itme["data"])
        #获取预期结果
        expected=eval(itme["expected"])
        #获取接口方法
        method=itme["method"]

        #todo 请求之前的数据库校验
        sql="select * from loan where member_id={}".format(self.member_id)
        start_count=self.db.find_count(sql)
        print("请求之前的数量"+str(start_count))


        #第二步:调用接口，获取实际结果
        response=requests.request(method=method,json=params,url=url,headers=self.headers)
        res=response.json()

        #todo 请求之后的数据库校验
        end_count = self.db.find_count(sql)
        print("请求之前的数量" + str(end_count))

        #第三步：断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])

            #根据添加项目是否成功，来对是数据库进行校验
            if res["msg"]=="OK":
                self.assertEqual(end_count-start_count,1)
            else:
                self.assertEqual(end_count-start_count,0)

        except AssertionError as e:
             mylog.error("用例--【{}】----执行失败".format(itme["title"]))
             mylog.error(e)
             # 记录详细的错误信息到日志用exception
             # mylog.exception(e)
             raise e
        else:
             # self.excel.write_data(row=row,column=5,value="通过")
             # 记录运行成功日志
            mylog.info("用例--【{}】----执行成功".format(itme["title"]))
























