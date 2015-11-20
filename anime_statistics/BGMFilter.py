# -*- coding: utf-8 -*-
import MySQLdb
import re

conn = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='123456',
                       db='anime_statistics',
                       charset="utf8",
                       port=3306)
cur = conn.cursor()


def fetch(name):
    cur.execute('SELECT * FROM bgm_anime_info WHERE format_name LIKE %s', name)
    return cur.fetchall()


def update(name_chinese, bgm_url, aid):
    value = [name_chinese, bgm_url, aid]
    cur.execute('update anime_relate_info SET name_chinese = %s, bgm_url = %s WHERE id = %s',
                value)


def regsp(istr, repl):
    sp = re.compile(ur'[-+・\'!-:.\(\)\s]')
    # 使用正则表达式替换 '～' 会把替换文本放两次
    r = sp.sub(repl, istr).replace(u'～', repl)
    return r


# 输出提醒有多个匹配值，需要手工确认
def print_check(origin, results, tag):
    text = 'tag[' + tag + '], id[' + str(origin[0]) + '], name[' + origin[1].encode("GBK",
                                                                                    'ignore') + '] have multiple matching results: \n'
    for result in results:
        text += 'bgm name[' + result[1].encode("GBK", 'ignore') + '], url[' + result[4].encode("GBK", 'ignore') + '] \n'
    print text


cur.execute('SELECT * FROM anime_relate_info WHERE bgm_url IS NULL')
origins = cur.fetchall()
for origin in origins:
    if origin[5] is not None:
        print "is filled. skip."
        continue

    aid = origin[0]
    name = origin[1]
    # 精确查找
    results = fetch(name)
    if len(results) > 0:
        update(results[0][2], results[0][3], aid)
        continue

    # 去除括号内容后精确查找
    bracketReg = re.compile(r'\(.*\)')
    noBracket = bracketReg.sub('', name)
    noBracket = noBracket.strip()
    results = fetch(noBracket)
    if len(results) > 0:
        update(results[0][2], results[0][3], aid)
        continue

    # 使用括号内容精确查找
    regGroup = re.search(r'\((.*)\)', name)
    bracketCont = ''
    if regGroup is not None:
        bracketCont = regGroup.group(1)
        bracketCont = bracketCont.strip()
        results = fetch(bracketCont)
        if len(results) > 0:
            update(results[0][2], results[0][3], aid)
            continue

    # 使用单个字符的通配符取代特殊字符伪精确查找
    newReg = regsp(name, '_')
    results = fetch(newReg)
    if len(results) > 0:
        update(results[0][2], results[0][3], aid)
        continue

    newReg = regsp(noBracket, '_')
    results = fetch(newReg)
    if len(results) > 0:
        update(results[0][2], results[0][3], aid)
        continue

    newReg = regsp(bracketCont, '_')
    results = fetch(newReg)
    if len(results) > 0:
        update(results[0][2], results[0][3], aid)
        continue

    # 使用通配符取代空格的模糊查找
    reS = re.compile(r'\s')
    regSpace = reS.sub('%', name)
    results = fetch(regSpace)
    if len(results) > 0:
        if len(results) == 1:
            update(results[0][2], results[0][3], aid)
        else:
            print_check(origin, results, 'replace space')
        continue

    # 使用通配符取代括号内容的模糊查找
    noBracketReg = bracketReg.sub('%', name)
    results = fetch(noBracketReg)
    if len(results) > 0:
        if len(results) == 1:
            update(results[0][2], results[0][3], aid)
        else:
            print_check(origin, results, 'replace brackets')
        continue

    # 加上首尾通配符的模糊查找
    # if len(name) > 4:
    reglr = '%' + name + '%'
    results = fetch(reglr)
    if len(results) > 0:
        if len(results) == 1:
            update(results[0][2], results[0][3], aid)
        else:
            print_check(origin, results, 'replace head tail')
        continue

    # 去掉括号后使用通配符取代特殊字符的模糊查找
    # 但是结果全都必须确认
    fuzzyReg = regsp(noBracket, '%')
    results = fetch(fuzzyReg)
    if len(results) > 0:
        if len(results) == 1:
            update(results[0][2], results[0][3], aid)
        else:
            print_check(origin, results, 'replace all sp')

conn.commit()
cur.close()
conn.close()
