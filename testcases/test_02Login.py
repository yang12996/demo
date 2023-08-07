import unittest
import requests
import os
from  unittestreport import ddt,list_data
from common.handle_config import conf
from common.Handle_Excel import HandleExcel
from common.handler_log import mylog
from  common.handler_path import DATA_DIR
from common.tools import Test


@ddt
class TestLogin(unittest.TestCase):
    #使用封装HandleExcel的类获取数据
    excel = HandleExcel(os.path.join(DATA_DIR,"aa.xlsx"), "login")
    #读取用例数据
    cases = excel.read_data()
    #从config获取url基本地址
    base_url=conf.get('env','url')
    # 从config获取请求头
    headrs=eval(conf.get('env','headers'))

    @list_data(cases)
    def test_login(self,item):
        #todo 第一步：准备数据
        #1、接口地址
        url=self.base_url+item['url']

        #2、接口请求参数
        item['data']=Test.replace_data(item['data'],TestLogin)


        params=eval(item['data'])

        #3、用例预期结果
        expected = eval(item['expected'])

        #4、请求头
        #5、获取请求方法，并且转换为小写
        method=item['method'].lower()

        #todo 第二步:请求接口，获取返回实际结果
        response = requests.post(url=url, json=params, headers=self.headrs)
        res=response.json()
        # print("预期结果",expected)
        # print("实际结果",res)
        #todo 第三步：断言
        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
        except AssertionError as e:
            #把结果写入excel工作簿中
            # self.excel.write_data(row=row,column=5,value="未通过")
            #记录运行的失败日志
            mylog.error("用例--【{}】----执行失败".format(item["title"]))
            mylog.error(e)
            #记录详细的错误信息到日志用exception
            # mylog.exception(e)
            raise  e
        else:
            # self.excel.write_data(row=row,column=5,value="通过")
            # 记录运行成功日志
            mylog.info("用例--【{}】----执行成功".format(item["title"]))

        #封装断言
        # res = {"user": "字段不", "time": "11122233"}
        # # 预期结果
        # expected = {"user": "字段不能不为空"}

        #def assertDictIn(self,expected,res):
        """字段成员运算逻辑"""
        #   for k, v in expected.items():
        #       if res.get(k) == v:
        #            print(k, v, 'res中找到了这个键和值')
        #            pass
        #        else:
        #            raise AssertionError("{} [k,v] not in {}".format(expected, res))