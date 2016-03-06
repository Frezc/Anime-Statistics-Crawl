# -*- coding: utf-8 -*-
import MySQLdb


class MysqlConn(object):
    conn = None
    cur = None

    def start_conn(self):
        """
        define your database config here
        :return:
        """
        self.conn = MySQLdb.connect(host='localhost',
                                    user='root',
                                    passwd='root',
                                    db='anime_statistics',
                                    charset="utf8",
                                    port=3306)
        self.cur = self.conn.cursor()
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
