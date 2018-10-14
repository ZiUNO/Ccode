# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Contact: github.com/ZiUNO/Compile-Code
* @Software: PyCharm
* @Time: 2018/10/14 14:55
"""


class LL1:
    STATE = {
        "SYNCH": 1
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
        for e in ffset.getGrammar():
            self.__chart[e] = dict()
            for termi in ffset.getTermi():
                self.__chart[e][termi] = ''
            self.__makeRowOf(e)
        del self.__grammar
        del self.__firstSet
        del self.__followSet
        del self.__termi
        for i in self.__chart:
            print(i, end=" | ")
            for j in self.__chart[i]:
                print(j, ":", self.__chart[i][j], end=",\t\t")
            print()

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
