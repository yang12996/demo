def login_check(username=None,password=None):
    """
    登录校验的函数
    :param username:账号
    :param passwork: 密码
    :return: dict tupe
    """
    if username!=None and password !=None:
        if username =="python35" and password =="123456":
            return {"code": 0, "msg": "登录成功"}
        else:
            return {"code":1,"msg":"账号或密码不正确"}
    else:
            return {"code": 1, "msg": "所有的参数不能为空"}


if __name__ == '__main__':
    #1、账号密码正确
    res=login_check("python35","123456")
    expected={"code":0,"msg":"登录成功"}
    if res ==expected:
        print("用例：正确的账号密码执行通过")
    # 1、密码错误
    res = login_check("python35", "1234567")
    expected = {"code":1,"msg":"账号或密码不正确"}
    if res == expected:
        print("密码错误")


