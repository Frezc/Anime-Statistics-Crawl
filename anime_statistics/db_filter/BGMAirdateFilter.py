# -*- coding: utf-8 -*-
from MySqlConn import MysqlConn

conn = MysqlConn()
cur = conn.start_conn()


def fetch(date):
    cur.execute('select * from bgm_anime_info where air_date = %s', date)
    return cur.fetchall()


def update(name_chinese, bgm_url, aid):
    value = [name_chinese, bgm_url, aid]
    cur.execute('update anime_relate_info SET name_chinese = %s, bgm_url = %s WHERE id = %s',
                value)


def print_check(o, r):
    text = 'id[' + str(o[0]) + '], name[' + o[1].encode("GBK",
                                                                  'ignore') + '] have multiple matching results: \n'
    for result in r:
        text += 'bgm name[' + result[1].encode("GBK", 'ignore') + '], chinese_name[' + result[3].encode("GBK", 'ignore') + '], url[' + result[4].encode("GBK", 'ignore') + '] \n'
    print text


cur.execute('SELECT * FROM anime_relate_info WHERE bgm_url IS NULL')
origins = cur.fetchall()
for origin in origins:
    aid = origin[0]
    date = origin[7]
    results = fetch(date)

    if len(results) > 1:
        print_check(origin, results)
    elif len(results) == 1:
        update(results[0][3], results[0][4], aid)

conn.close()
