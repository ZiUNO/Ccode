# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Contact: github.com/ZiUNO/Compile-Code
* @Software: PyCharm
* @Time: 2018/10/14 14:28
"""


class FFSet:
    def __init__(self, size):
        self.__termi = []
        self.__grammar = dict()
        self.__isChecked = dict()
        self.__firstAgg = dict()
        self.__firstChild = dict()
        self.__followAgg = dict()
        self.__followChild = dict()
        self.__size = size
        self.__hasNULL = []
        self.__haveMadeFirst = False
        self.__haveMadeFollow = False
        self.__record = dict()
        self.__hasSetTermi = False
        self.__hasSetFirstNontermi = False

    def __canInput(self):
        if self.__size == 0 or not self.__hasSetTermi:
            exit(1)
        self.__size -= 1
        return True

    def __isPrepared(self):
        if self.__size == 0 or not self.__hasSetTermi:
            return True
        return False

    def __clearRecord(self):
        for e in self.__record:
            self.__record[e] = []

    def inputGrammar(self, e, expressions):
        if self.__canInput():
            pass
        self.__grammar[e] = expressions.split("|")
        self.__isChecked[e] = False
        self.__firstAgg[e] = []
        self.__followAgg[e] = []
        self.__firstChild[e] = []
        self.__followChild[e] = []
        self.__record[e] = []
        for expression in self.__grammar[e]:
            if expression[0] in self.__termi:
                if 'ε' == expression:
                    self.__hasNULL.append(e)
                    return
                self.__firstAgg[e].append(expression[0])
            else:
                self.__firstChild[e].append(expression)
        return

    def getGrammar(self):
        return self.__grammar

    def getFollow(self):
        if not self.__haveMadeFollow:
            if not self.__haveMadeFirst:
                self.getFirst()
                self.__haveMadeFirst = True
        for e in self.__grammar:
            for expression in self.__grammar[e]:
                for tmpSymbolIndex in range(len(expression)):
                    if expression[tmpSymbolIndex] not in self.__termi:
                        if tmpSymbolIndex == len(expression) - 1:
                            if expression[tmpSymbolIndex] == e:
                                continue
                            self.__record[expression[tmpSymbolIndex]].append(e)
                            self.__record[e].append(expression[tmpSymbolIndex])
                        else:
                            for hasNULLIndex in range(tmpSymbolIndex + 1, len(expression)):
                                if expression[hasNULLIndex] in self.__termi:
                                    self.__followAgg[expression[tmpSymbolIndex]].append(expression[hasNULLIndex])
                                    break
                                for toAppend in self.__firstAgg[expression[hasNULLIndex]]:
                                    if toAppend != 'ε':
                                        self.__followAgg[expression[tmpSymbolIndex]].append(toAppend)
                                if expression[hasNULLIndex] not in self.__hasNULL:
                                    break
                                elif hasNULLIndex == len(expression) - 1:
                                    self.__record[e].append(expression[tmpSymbolIndex])
                        self.__updateFollowAgg()
            self.__haveMadeFollow = True
        return self.__followAgg

    def setFirstNontermi(self, e):
        if not self.__hasSetFirstNontermi:
            self.__followAgg[e].append('$')
            self.__hasSetFirstNontermi = True
        else:
            exit(1)

    def getTermi(self):
        return self.__termi

    def setTermi(self, termi):
        self.__hasSetTermi = True
        self.__termi = termi.copy()
        return

    def getFirst(self):
        if not self.__haveMadeFirst:
            for e in self.__firstChild:
                self.__calculate(e)
            self.__updateFirstAgg()
            for e in self.__hasNULL:
                self.__firstAgg[e].append('ε')
            self.__haveMadeFirst = True
            self.__clearRecord()
        return self.__firstAgg

    def __updateFirstAgg(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__firstAgg[child] += self.__firstAgg[father]
                self.__firstAgg[child] = list(set(self.__firstAgg[child]))
                self.__firstAgg[father] = list(set(self.__firstAgg[father]))
        return

    def __updateFollowAgg(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__followAgg[child] += self.__followAgg[father]
                self.__followAgg[child] = list(set(self.__followAgg[child]))
        for e in self.__followAgg:
            self.__followAgg[e] = list(set(self.__followAgg[e]))
        return

    def __calculate(self, e):
        isContainsNULL = False
        if e in self.__hasNULL:
            isContainsNULL = True
        if len(self.__firstChild[e]) == 0:
            self.__isChecked[e] = True
        if self.__isChecked[e]:
            return isContainsNULL
        for expression in self.__firstChild[e]:
            for tmpSymbolIndex in range(len(expression)):
                if expression[tmpSymbolIndex] in self.__termi:
                    self.__firstAgg[e].append(expression[tmpSymbolIndex])
                    self.__isChecked[e] = True
                    self.__updateFirstAgg()
                    return False
                self.__record[expression[tmpSymbolIndex]].append(e)
                self.__updateFirstAgg()
                if self.__calculate(expression[tmpSymbolIndex]):
                    if tmpSymbolIndex == len(expression) - 1:
                        self.__hasNULL.append(e)
                        self.__isChecked[e] = True
                        return True
                else:
                    self.__isChecked[e] = True
                    return False
        return False
