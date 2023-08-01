import requests
from jsonpath import jsonpath
from common.handle_config import conf

class BaseTest():

        #*******************管理员登录*****************************
        @classmethod
        def admin_loan(cls):
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
        @classmethod
        def user_login(cls):
            #1、准备登录数据
            url = conf.get("env", "url") + "/member/login"
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

        #*******************普通用户添加项目*****************************
        @classmethod
        def add_project(cls):
            # 第一步：准备数据
            url = conf.get("env", "url") + "/loan/add"
            params ={"member_id" :cls.member_id,
                    "title" :"借款",
                    "amount" :2000,
                    "loan_rate" :12.0,
                    "loan_term" :3,
                    "loan_date_type" :1,
                    "bidding_days" :5}
            # 第二步：请求添加项目的接口
            response =requests.request(method="post" ,url=url ,json=params ,headers=cls.headers)
            res =response.json()
            # 第三步：提取项目的id,保存为类属性
            cls.loan_id = jsonpath(res, "$..id")[0]

        #*******************管理员审核*****************************
        @classmethod
        def audit(cls):
            # 第一步：准备数据
            url = conf.get("env", "url") + "/loan/audit"
            params = {"loan_id": cls.loan_id,
                      "approved_or_not":True}
            # 第二步：请求添加项目的接口,对接口进行审核
            response = requests.patch( url=url, json=params, headers=cls.admin_headers)


