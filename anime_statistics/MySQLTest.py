import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='anime_statistics',port=3306)
    cur=conn.cursor()
    print cur.execute('select * from ann_anime_info')
    print cur.f
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])