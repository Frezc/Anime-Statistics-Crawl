# -*- coding: utf-8 -*-
import Levenshtein
import re


class AnimeCompare(object):
    sp_pattern = re.compile(r'[\(\)`!@#\$%\^&\*\-=\+/\\_\[\]\{\},\.\'\";:\?~<>\s～‘！＠＃＄％＾＆＊（）＿＋＝・￥「」｛｝；’：、。＜＞？★♪×…]')

    def __init__(self, base_name):
        self.cons = []
        self.beli = []
        self.sure = []
        self.base_name = base_name.replace(u'劇場版', '').strip()

    def compare(self, names):

        # i = 0
        # while i < len(names):
        for i in range(len(names)):
            name_arr = names[i]
            # print name_arr

            status = self.compare_per_name(name_arr)

            if status == 3:
                self.sure.append(i)
            elif status == 2:
                self.beli.append(i)
            elif status == 1:
                self.cons.append(i)

                # i += 1

        if len(self.beli) == 0 and len(self.cons) == 0 and len(self.sure) == 0:
            return False
        else:
            return True

    def compare_per_name(self, name_arr):
        pass

    @staticmethod
    def check_date(base_date, vintage_arr):
        # print 'check_date ' + base_date + ' ' + str(vintage_arr)

        matched = []
        matched_y = []
        i = 0
        # while i < len(vintage_arr):
        for i in range(len(vintage_arr)):
            date = AnimeAlCompare.vintage_to_date(vintage_arr[i])
            if date == 'unknown':
                continue
            elif len(date) == 4:
                if base_date[0:4] == date:
                    matched_y.append(i)
            elif base_date == date:
                matched.append(i)

                # i += 1

        if len(matched) > 0:
            return matched
        else:
            return matched_y

    @staticmethod
    def vintage_to_date(vintage):
        if len(vintage) == 0:
            return 'unknown'

        AnimeAlCompare.pattern_brackets.sub('', vintage)

        index = vintage.find(u'to')
        if index != -1:
            return vintage[0:index - 1]
        else:
            return vintage


class AnimeAlCompare(AnimeCompare):
    pattern_brackets = re.compile(r'\([^\(\)]+\)')

    def compare_per_name(self, name_arr):
        is_cons = False
        no_brackets = self.pattern_brackets.sub('', self.base_name)
        no_sp = self.sp_pattern.sub(r'.*', no_brackets)
        for name in name_arr:
            no_brackets1 = self.pattern_brackets.sub('', name)
            no_sp1 = self.sp_pattern.sub('', no_brackets1)

            # if self.check_sure(self.base_name, name):
            if self.base_name == name:
                return 3

            if no_brackets == no_brackets1:
                return 3

            if no_sp == no_sp1:
                return 3

            if re.match(no_sp, name) is not None:
                return 2

            if self.check_beli(self.base_name, name):
                return 2

            if self.check_beli(no_sp, no_sp1):
                return 2

            if not is_cons and self.check_cons(self.base_name, name):
                is_cons = True

            if not is_cons and self.check_cons(no_brackets, no_brackets1):
                is_cons = True
        if is_cons:
            return 1
        else:
            return 0
            # return 0

    @staticmethod
    def check_sure(name1, name2):
        ratio = Levenshtein.ratio(name1, name2)
        jaro = Levenshtein.jaro(name1, name2)
        jaro_winkler = Levenshtein.jaro_winkler(name1, name2)
        if ratio >= 0.9 and jaro >= 0.95 and jaro_winkler >= 0.95:
            return True
        else:
            return False

    @staticmethod
    def check_beli(name1, name2):
        ratio = Levenshtein.ratio(name1, name2)
        jaro = Levenshtein.jaro(name1, name2)
        jaro_winkler = Levenshtein.jaro_winkler(name1, name2)
        if ratio >= 0.9 or jaro >= 0.9 or jaro_winkler >= 0.9:
            return True
        elif ratio >= .7 and jaro >= .8 and jaro_winkler >= .8:
            return True
        else:
            return False

    @staticmethod
    def check_cons(name1, name2):
        ratio = Levenshtein.ratio(name1, name2)
        jaro = Levenshtein.jaro(name1, name2)
        jaro_winkler = Levenshtein.jaro_winkler(name1, name2)
        if ratio > .6 or jaro > .7 or jaro_winkler > .7:
            return True
        else:
            return False


class AnimeNormalaCompare(AnimeCompare):
    pattern_brackets = re.compile(r'\(.+\)')

    def compare_per_name(self, name_arr):

        for name in name_arr:
            pass

    @staticmethod
    def check_sure(name1, name2):
        if name1 == name2:
            return True

    @staticmethod
    def check_beli(name1, name2):
        pass

    @staticmethod
    def check_cons(name1, name2):
        pass
