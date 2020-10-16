import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='database-2.claxa3upyxck.ap-northeast-2.rds.amazonaws.com',
                                  user='rtjxodnd',
                                  password='2wlstn70!1',
                                  # db='stock_search',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
