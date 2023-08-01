import pymysql
from common.handle_config import conf

class  HandleDB:
    def __init__(self):
     #连接数据库
     self.con=pymysql.connect(
                           host=conf.get("mysql", "host"),
                           port=conf.getint("mysql", "port"),
                           user=conf.get("mysql", "user"),
                           password=conf.get("mysql", "password"),
                           database=conf.get("mysql", "database"),
                           charset="utf8",
                           #cursorclass=pymysql.cursors.DictCursor
                     )

    """查询到所有数据"""
    def find_all(self,sql):
        with self.con as cur:     #使用with可以自动执行事务提交
              # 执行sql语句
              cur.execute(sql)
              #查询结果
              res=cur.fetchall()
              #关闭游标
              cur.close()
        return res

    """查询到一条数据"""
    def find_one(self, sql):
        with self.con as cur:
            cur.execute(sql)
            res=cur.fetchone()
            cur.close()
        return res

    """查询到数据量"""
    def find_count(self, sql):
        with self.con as cur:
            res=cur.execute(sql)
            cur.close()
        return res

    """对象销毁时自动执行"""
    def __del__(self):
        self.con.close()

if __name__ == '__main__':
    sql="select * from  member limit 5"
    db=HandleDB()
    res = db.find_one(sql)
    print(res)

