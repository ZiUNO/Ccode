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
        self.__firstSet = dict()
        self.__firstChild = dict()
        self.__followSet = dict()
        self.__followChild = dict()
        self.__size = size
        self.__hasNULL = []
        self.__haveMadeFirst = False
        self.__haveMadeFollow = False
        self.__record = dict()
        self.__hasSetTermi = False
        self.__firstNontermi = None
        self.__lastNontermi = None

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
        self.__firstSet[e] = []
        self.__followSet[e] = []
        self.__firstChild[e] = []
        self.__followChild[e] = []
        self.__record[e] = []
        for expression in self.__grammar[e]:
            if expression[0] in self.__termi:
                if 'ε' == expression:
                    self.__hasNULL.append(e)
                    return
                self.__firstSet[e].append(expression[0])
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
                                    self.__followSet[expression[tmpSymbolIndex]].append(expression[hasNULLIndex])
                                    break
                                for toAppend in self.__firstSet[expression[hasNULLIndex]]:
                                    if toAppend != 'ε':
                                        self.__followSet[expression[tmpSymbolIndex]].append(toAppend)
                                if expression[hasNULLIndex] not in self.__hasNULL:
                                    break
                                elif hasNULLIndex == len(expression) - 1:
                                    self.__record[e].append(expression[tmpSymbolIndex])
                        self.__updateFollowSet()
            self.__haveMadeFollow = True
        return self.__followSet

    def setFirstNontermi(self, e):
        if self.__firstNontermi is None:
            self.__followSet[e].append('$')
            self.__firstNontermi = e
        else:
            exit(1)

    def getFirstNontermi(self):
        return self.__firstNontermi

    def getLastNontermi(self):
        return self.__lastNontermi

    def setLastNontermi(self, e):
        if self.__lastNontermi is None:
            self.__lastNontermi = e
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
            self.__updateFirstSet()
            for e in self.__hasNULL:
                self.__firstSet[e].append('ε')
            self.__haveMadeFirst = True
            self.__clearRecord()
        return self.__firstSet

    def __updateFirstSet(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__firstSet[child] += self.__firstSet[father]
                self.__firstSet[child] = list(set(self.__firstSet[child]))
                self.__firstSet[father] = list(set(self.__firstSet[father]))
        return

    def __updateFollowSet(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__followSet[child] += self.__followSet[father]
                self.__followSet[child] = list(set(self.__followSet[child]))
        for e in self.__followSet:
            self.__followSet[e] = list(set(self.__followSet[e]))
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
                    self.__firstSet[e].append(expression[tmpSymbolIndex])
                    self.__isChecked[e] = True
                    self.__updateFirstSet()
                    return False
                self.__record[expression[tmpSymbolIndex]].append(e)
                self.__updateFirstSet()
                if self.__calculate(expression[tmpSymbolIndex]):
                    if tmpSymbolIndex == len(expression) - 1:
                        self.__hasNULL.append(e)
                        self.__isChecked[e] = True
                        return True
                else:
                    self.__isChecked[e] = True
                    return False
        return False
