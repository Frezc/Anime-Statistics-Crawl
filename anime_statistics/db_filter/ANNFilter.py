# -*- coding: utf-8 -*-
from MySqlConn import MysqlConn

conn = MysqlConn()
cur = conn.start_conn()

cur.execute('SELECT id, name, sati_url, air_date FROM anime_relate_info WHERE ann_url IS NULL')
relates = cur.fetchall()
cur.execute('SELECT name_english, name_japanese, url, vintage FROM ann_anime_info')
ann_results = cur.fetchall()

ann_jpnames = []

# print ann_results[5][1].split(',')[0] == ''

# 将日文名称拆分存入ann_jpnames list
for ann_result in ann_results:
    ann_jpnames.append(ann_result[1].split(','))

print 'break name over.'

conn.close()
