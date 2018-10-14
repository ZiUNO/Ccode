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
        self.__grammar = self.__ffs.getGrammar()
        self.__firstSet = self.__ffs.getFirst()
        self.__followSet = self.__ffs.getFollow()
        self.__termi = self.__ffs.getTermi()
        self.__termi.remove('ε')
        self.__termi.append('$')
        self.__chart = dict()
        self.__wrongMessage = []
        self.__message = []
        mat = ''
        for e in ffset.getGrammar():
            self.__chart[e] = dict()
            for termi in ffset.getTermi():
                mat += '{:^10}\t'
                if e == ffset.getLastNontermi():
                    self.__chart[e][termi] = 'SYNCH'
                else:
                    self.__chart[e][termi] = 'ERROR'
            self.__makeRowOf(e)
        del self.__grammar
        del self.__firstSet
        del self.__followSet
        del self.__termi
        for i in self.__chart:
            tmpMessage = i + '|'
            for j in self.__chart[i]:
                tmpMessage += "%s:%-10s" % (j, self.__chart[i][j])
            self.__message.append(tmpMessage)

    def getChart(self):
        separator = '\n'
        return separator.join(self.__message)

    def __makeRowOf(self, e):
        grammar = self.__grammar[e]
        for expression in grammar:
            for tmpTermi in self.__termi:
                if tmpTermi == expression[0]:
                    self.__chart[e][tmpTermi] = expression
                elif expression[0] in self.__termi:
                    pass
                elif expression == 'ε':
                    for follow in self.__followSet[e]:
                        self.__chart[e][follow] = 'ε'
                elif tmpTermi in self.__firstSet[e]:
                    self.__chart[e][tmpTermi] = expression
                elif tmpTermi in self.__followSet[e]:
                    self.__chart[e][tmpTermi] = "SYNCH"
        return

    def check(self, toCheck):
        process = []
        message = []
        count = 0
        position = None
        toCheck = list(reversed(toCheck))
        if toCheck[0] != '$':
            toCheck.insert(0, '$')
        stack = ['$', self.__ffs.getFirstNontermi()]
        tmpSymbol = stack.pop()
        tmpToCheck = toCheck.pop()
        columnCount = 0
        separator = '\n'
        while len(stack) != 0:
            # 匹配成功
            if tmpToCheck == tmpSymbol:
                tmpSymbol = stack.pop()
                tmpToCheck = toCheck.pop()
                columnCount += 1
                continue
            if tmpSymbol in self.__ffs.getTermi():
                count += 1
                message.append('[ERROR(No.%d)]missing %s at %d column' % (count, tmpSymbol, columnCount))
                tmpSymbol = stack.pop()
                columnCount += 1
                continue
            expression = self.__chart[tmpSymbol][tmpToCheck]
            if expression == "SYNCH" or expression == "ε":
                tmpSymbol = stack.pop()
                if expression == "SYNCH":
                    count += 1
                    message.append('[ERROR(No.%d)]unexpected %s at %d column' % (count, tmpToCheck, columnCount))
            elif expression == "ERROR":
                count += 1
                columnCount += 1
                message.append('[ERROR(No.%d)]unexpected %s at %d column' % (count, tmpToCheck, columnCount))
                tmpToCheck = toCheck.pop()
            else:
                process.append('%s->%s' % (tmpSymbol, expression))
                stack += list(reversed(expression))
                tmpSymbol = stack.pop()
        message.append('total %d error(s)' % count)
        return separator.join(process), separator.join(message)
