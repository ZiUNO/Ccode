# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Contact: github.com/ZiUNO/Compile-Code
* @Software: PyCharm
* @Time: 2018/10/14 14:55
"""


class LL1:
    STATE = {
        "SYNCH": 1,
        "ERROR": 2
    }

    def __init__(self, ffset):
        self.__ffs = ffset
        self.__grammar = self.__ffs.get_grammar()
        self.__first_set = self.__ffs.get_first()
        self.__followSet = self.__ffs.get_follow()
        self.__terminator = self.__ffs.get_terminator_of_first()
        self.__terminator.remove('ε')
        self.__terminator.append('$')
        self.__chart = dict()
        self.__wrongMessage = []
        self.__message = []
        mat = ''
        for e in ffset.get_grammar():
            self.__chart[e] = dict()
            for termi in ffset.get_terminator_of_first():
                mat += '{:^10}\t'
                if e == ffset.get_last_non_terminator():
                    self.__chart[e][termi] = 'SYNCH'
                else:
                    self.__chart[e][termi] = 'ERROR'
            self.__make_row_of(e)
        del self.__grammar
        del self.__first_set
        del self.__followSet
        del self.__terminator
        for i in self.__chart:
            tmp_message = i + '|'
            for j in self.__chart[i]:
                tmp_message += "%s:%-10s" % (j, self.__chart[i][j])
            self.__message.append(tmp_message)

    def get_chart(self):
        separator = '\n'
        return separator.join(self.__message)

    def __make_row_of(self, e):
        grammar = self.__grammar[e]
        for expression in grammar:
            for tmpTermi in self.__terminator:
                if tmpTermi == expression[0]:
                    self.__chart[e][tmpTermi] = expression
                elif expression[0] in self.__terminator:
                    pass
                elif expression == 'ε':
                    for follow in self.__followSet[e]:
                        self.__chart[e][follow] = 'ε'
                elif tmpTermi in self.__first_set[e]:
                    self.__chart[e][tmpTermi] = expression
                elif tmpTermi in self.__followSet[e]:
                    self.__chart[e][tmpTermi] = "SYNCH"
        return

    def check(self, to_check):
        process = []
        message = []
        count = 0
        to_check = list(reversed(to_check))
        if to_check[0] != '$':
            to_check.insert(0, '$')
        stack = ['$', self.__ffs.get_first_non_terminator()]
        tmp_symbol = stack.pop()
        tmp_to_check = to_check.pop()
        column_count = 0
        separator = '\n'
        while len(stack) != 0:
            # 匹配成功
            if tmp_to_check == tmp_symbol:
                tmp_symbol = stack.pop()
                tmp_to_check = to_check.pop()
                column_count += 1
                continue
            if tmp_symbol in self.__ffs.get_terminator_of_first():
                count += 1
                message.append('[ERROR(No.%d)]missing %s at %d column' % (count, tmp_symbol, column_count))
                tmp_symbol = stack.pop()
                column_count += 1
                continue
            expression = self.__chart[tmp_symbol][tmp_to_check]
            if expression == "SYNCH" or expression == "ε":
                tmp_symbol = stack.pop()
                if expression == "SYNCH":
                    count += 1
                    message.append('[ERROR(No.%d)]unexpected %s at %d column' % (count, tmp_to_check, column_count))
            elif expression == "ERROR":
                count += 1
                column_count += 1
                message.append('[ERROR(No.%d)]unexpected %s at %d column' % (count, tmp_to_check, column_count))
                tmp_to_check = to_check.pop()
            else:
                process.append('%s->%s' % (tmp_symbol, expression))
                stack += list(reversed(expression))
                tmp_symbol = stack.pop()
        message.append('total %d error(s)' % count)
        return separator.join(process), separator.join(message)
