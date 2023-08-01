# from  common.handle_pymysql import  HandleDB
#
# class test():
#     db=HandleDB()
#
#
#     def aa(self):
#         sql ="select * from  member limit 5"
#         res =self.db.find_all(sql)
#         print(res)
#
# if __name__ == '__main__':
#     d=test()
#     d.aa()
# import  re
#
# class TestData():
#       id="123"
#       name="yang"
#
# s2 = '{"id":"#id#","name":"#name#"}'
# #注意: search匹配到了返回一个对象，没有匹配到返回None
# while re.search('#(.+?)#', s2):
#     res2 = re.search('#(.+?)#',s2)
#     # print(res2)
#     item= res2.group()
#     attr = res2.group(1)
#     value = getattr(TestData,attr)
#     #进行替换
#     s2 = s2.replace(item, str( value))
# print(s2)
class TestData1():
      id="123"
      name="yang"
s2 = '{"id":"#id#","name":"#name#"}'
from  common.tools import Test
aa=Test.replace_data(s2,TestData1)
print(aa)
