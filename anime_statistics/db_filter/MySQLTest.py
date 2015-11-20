# -*- coding: utf-8 -*-
import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='123456',
                           db='anime_statistics',
                           charset="utf8",
                           port=3306)
    cur = conn.cursor()
    cur.execute('explain select * from bgm_anime_info WHERE format_name LIKE %s', u'(超)劇場版!地獄先生ぬ～べ～')
    print cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
