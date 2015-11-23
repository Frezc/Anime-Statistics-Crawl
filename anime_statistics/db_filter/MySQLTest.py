# -*- coding: utf-8 -*-
import MySQLdb
from MySqlConn import MysqlConn

try:
    conn = MysqlConn()
    cur = conn.start_conn()
    cur.execute('explain select * from bgm_anime_info WHERE format_name LIKE %s', u'(超)劇場版!地獄先生ぬ～べ～')
    print cur.fetchall()

    cur.execute('explain select * from bgm_anime_info WHERE format_name LIKE %s', u'(超)劇場版!')
    print cur.fetchall()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
