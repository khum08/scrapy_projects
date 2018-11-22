# coding:utf-8
import pymysql

from ..settings import HOST, USER, PASSWD, DB, PORT, CHARSET


class DbUtils(object):

    def __init__(self):
        self.conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, port=PORT, charset=CHARSET)
        self.cursor = self.conn.cursor()

    # test 测试
    def query_all(self):
        self.cursor.execute("select * from subsidy")
        self.conn.commit()
        data = self.cursor.fetchall()
        for d in data:
            print(d)

    # 查询数据库是否存在该用户，存在则返回状态 0 表示公示 1 表示其他
    # 不存在该用户 则返回 -1
    def query_one(self, id_card):
        sql = "select status from subsidy where id_card='%s'" % id_card
        result = None
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            data = self.cursor.fetchall()
            if data:
                result = data[0][0]
        except:
            result = -1
        return result

    # insert into one user;
    def insert_user(self, name, id_card, status):
        conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, port=PORT, charset=CHARSET)
        cursor = conn.cursor()
        result = 0
        try:
            sql = "insert into subsidy(name, id_card, status) values('%s','%s','%d')" % (name, id_card, status)
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            result = -1
        return result

    # update user's status
    def update(self, id_card, status):
        conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, port=PORT, charset=CHARSET)
        cursor = conn.cursor()
        sql = "update subsidy set status='%d' where id_card='%s'" % (status, id_card)
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()

    def close_resource(self):
        self.cursor.close()
        self.conn.close()


