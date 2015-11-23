# -*- coding: utf-8 -*-
from MySqlConn import MysqlConn
from AnimeCompare import AnimeAlCompare

conn = MysqlConn()
cur = conn.start_conn()

cur.execute('SELECT id, name, sati_url, air_date FROM anime_relate_info WHERE ann_url IS NULL')
relates = cur.fetchall()
cur.execute('SELECT name_english, name_japanese, url, vintage FROM ann_anime_info WHERE consider = 1')
ann_results = cur.fetchall()


def update_ann(rel, ann_r):
    value = [
        ann_r[0],
        ann_r[2],
        rel[0]
    ]
    cur.execute('update anime_relate_info SET name_english = %s, ann_url = %s where id = %s', value)


def print_check(rel, index_arr, tag):
    text = 'tag[' + tag + ']\nid[' + str(rel[0]) + '], name[' + rel[1].encode("GBK",
                                                                              'ignore') + '] auto match failed results: \n'

    for index in index_arr:
        if ann_results[index][1] == '':
            title = ann_results[index][0]
        else:
            title = ann_results[index][1]

        text += 'ann name[' + title.encode("GBK", 'ignore') + '], url[' + ann_results[index][2].encode(
            "GBK", 'ignore') + ']\n'
    print text


ann_names = []

# print ann_results[5]

# 将日文名称拆分存入ann_jpnames list
for ann_result in ann_results:
    if ann_result[1] == u'':
        ann_names.append(ann_result[0].split(u','))
    else:
        ann_names.append(ann_result[1].split(u','))

print 'break name over.'

# print ann_names

for relate in relates:
    ac = AnimeAlCompare(relate[1])
    if ac.compare(ann_names):
        # print str(ac.cons)
        if len(ac.sure) > 0:
            if len(ac.sure) == 1:
                update_ann(relate, ann_results[ac.sure[0]])
            else:
                match = AnimeAlCompare.check_date(relate[3],
                                                  [ann_results[i][3] for i in ac.sure])
                if len(match) == 1:
                    update_ann(relate, ann_results[ac.sure[match[0]]])
                elif len(match) == 0:
                    print_check(relate, ac.sure, 'date no match [sure]')
                else:
                    print_check(relate, ac.sure, 'date multi match [sure]')
        elif len(ac.beli) > 1:
            match = AnimeAlCompare.check_date(relate[3],
                                              [ann_results[i][3] for i in ac.beli])
            if len(match) == 1:
                update_ann(relate, ann_results[ac.beli[match[0]]])
            elif len(match) == 0:
                print_check(relate, ac.beli, 'date no match [believe]')
            else:
                print_check(relate, ac.beli, 'date multi match [believe]')
        elif len(ac.beli) == 1:
            update_ann(relate, ann_results[ac.beli[0]])
        else:
            if len(ac.cons) > 0:
                match = AnimeAlCompare.check_date(relate[3],
                                                  [ann_results[i][3] for i in ac.cons])
                if len(match) == 1:
                    update_ann(relate, ann_results[ac.cons[match[0]]])
                elif len(match) == 0:
                    print_check(relate, ac.cons, 'date no match')
                else:
                    print_check(relate, ac.cons, 'date multi match')

    else:
        print_check(relate, [], 'no match')

conn.close()
