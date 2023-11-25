from  unittestreport import  TestRunner
from common.handler_path import  CASES_DIR,REPORT_DIR
import unittest
def main():
    """程序入口"""
    suite=unittest.defaultTestLoader.discover(CASES_DIR)
    runner=TestRunner(suite,
                      filename="reports.html",
                      report_dir=REPORT_DIR,
                      tester='GFS测试员',
                      desc="广西财经学院外卖项目测试生成的报告",
                      )
    runner.run()

    #-----------------测试报告QQ邮箱发送-----------------
    runner.send_email(  host='smtp.qq.com',
                        port=465,
                        user='yang2023.7.28@qq.com',
                        password='zthwwjnrctjugddd',
                        to_addrs='1437358161@qq.com',
                        is_file=True)

    #-------------扩展自定义邮件的标题和内容-------------------
    # from unittestreport.core.sendEmail import SendEmail
    # em=SendEmail(host='smtp.qq.com',
    #              port=465,
    #              user='yang2023.7.28@qq.com',
    #              password='zthwwjnrctjugddd')
    #
    # em.send_email(subject="测试报告",
    #               content="邮件内容",
    #               to_addrs="1437358161@qq.com")

    # -------------测试结果推送到钉钉群组-------------------
    # webhook="",
    # runner.dingtalk_notice(url=webhook,key="测试")

    # -------------企业微信通知，参照企业微信官方的API平台-------------------


if __name__ == '__main__':
    main()
    print("发送报告完毕")
