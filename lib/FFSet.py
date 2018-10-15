# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Contact: github.com/ZiUNO/Compile-Code
* @Software: PyCharm
* @Time: 2018/10/14 14:28
"""


class FFSet:
    def __init__(self, size):
        self.__terminator = []
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
        self.__has_set_terminator = False
        self.__first_non_terminator = None
        self.__last_non_terminator = None

    def __can_input(self):
        if self.__size == 0 or not self.__has_set_terminator:
            exit(1)
        self.__size -= 1
        return True

    def __is_prepared(self):
        if self.__size == 0 or not self.__has_set_terminator:
            return True
        return False

    def __clear_record(self):
        for e in self.__record:
            self.__record[e] = []

    def input_grammar(self, e, expressions):
        if self.__can_input():
            pass
        self.__grammar[e] = expressions.split("|")
        self.__isChecked[e] = False
        self.__firstSet[e] = []
        self.__followSet[e] = []
        self.__firstChild[e] = []
        self.__followChild[e] = []
        self.__record[e] = []
        for expression in self.__grammar[e]:
            if expression[0] in self.__terminator:
                if 'ε' == expression:
                    self.__hasNULL.append(e)
                    return
                self.__firstSet[e].append(expression[0])
            else:
                self.__firstChild[e].append(expression)
        return

    def get_grammar(self):
        return self.__grammar

    def get_follow(self):
        if not self.__haveMadeFollow:
            if not self.__haveMadeFirst:
                self.get_first()
                self.__haveMadeFirst = True
        for e in self.__grammar:
            for expression in self.__grammar[e]:
                for tmpSymbolIndex in range(len(expression)):
                    if expression[tmpSymbolIndex] not in self.__terminator:
                        if tmpSymbolIndex == len(expression) - 1:
                            if expression[tmpSymbolIndex] == e:
                                continue
                            self.__record[expression[tmpSymbolIndex]].append(e)
                            self.__record[e].append(expression[tmpSymbolIndex])
                        else:
                            for hasNULLIndex in range(tmpSymbolIndex + 1, len(expression)):
                                if expression[hasNULLIndex] in self.__terminator:
                                    self.__followSet[expression[tmpSymbolIndex]].append(expression[hasNULLIndex])
                                    break
                                for toAppend in self.__firstSet[expression[hasNULLIndex]]:
                                    if toAppend != 'ε':
                                        self.__followSet[expression[tmpSymbolIndex]].append(toAppend)
                                if expression[hasNULLIndex] not in self.__hasNULL:
                                    break
                                elif hasNULLIndex == len(expression) - 1:
                                    self.__record[e].append(expression[tmpSymbolIndex])
                        self.__update_follow_set()
            self.__haveMadeFollow = True
        return self.__followSet

    def set_first_non_terminator(self, e):
        if self.__first_non_terminator is None:
            self.__followSet[e].append('$')
            self.__first_non_terminator = e
        else:
            exit(1)

    def get_first_non_terminator(self):
        return self.__first_non_terminator

    def get_last_non_terminator(self):
        return self.__last_non_terminator

    def set_last_non_terminator(self, e):
        if self.__last_non_terminator is None:
            self.__last_non_terminator = e
        else:
            exit(1)

    def get_terminator(self):
        return self.__terminator

    def set_terminator(self, termi):
        self.__has_set_terminator = True
        self.__terminator = termi.copy()
        return

    def get_first(self):
        if not self.__haveMadeFirst:
            for e in self.__firstChild:
                self.__calculate(e)
            self.__update_first_set()
            for e in self.__hasNULL:
                self.__firstSet[e].append('ε')
            self.__haveMadeFirst = True
            self.__clear_record()
        return self.__firstSet

    def __update_first_set(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__firstSet[child] += self.__firstSet[father]
                self.__firstSet[child] = list(set(self.__firstSet[child]))
                self.__firstSet[father] = list(set(self.__firstSet[father]))
        return

    def __update_follow_set(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__followSet[child] += self.__followSet[father]
                self.__followSet[child] = list(set(self.__followSet[child]))
        for e in self.__followSet:
            self.__followSet[e] = list(set(self.__followSet[e]))
        return

    def __calculate(self, e):
        is_contains_null = False
        if e in self.__hasNULL:
            is_contains_null = True
        if len(self.__firstChild[e]) == 0:
            self.__isChecked[e] = True
        if self.__isChecked[e]:
            return is_contains_null
        for expression in self.__firstChild[e]:
            for tmpSymbolIndex in range(len(expression)):
                if expression[tmpSymbolIndex] in self.__terminator:
                    self.__firstSet[e].append(expression[tmpSymbolIndex])
                    self.__isChecked[e] = True
                    self.__update_first_set()
                    return False
                self.__record[expression[tmpSymbolIndex]].append(e)
                self.__update_first_set()
                if self.__calculate(expression[tmpSymbolIndex]):
                    if tmpSymbolIndex == len(expression) - 1:
                        self.__hasNULL.append(e)
                        self.__isChecked[e] = True
                        return True
                else:
                    self.__isChecked[e] = True
                    return False
        return False
