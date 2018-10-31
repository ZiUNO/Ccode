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
                            if tmpSymbolIndex == len(expression) - 1 and expression[tmpSymbolIndex] != e:
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

    def get_terminator_of_first(self):
        return self.__terminator

    def get_terminator_of_follow(self):
        terminators = [terminator for terminator in self.__terminator if terminator != 'ε']
        terminators.append('$')
        return terminators

    def set_terminator(self, termi):
        self.__has_set_terminator = True
        self.__terminator = termi.copy()
        return

    def __is_in_null_list(self, e):
        if e in self.__hasNULL:
            return True
        for expression in self.__firstChild[e]:
            for symbol_index in range(len(expression)):
                if expression[symbol_index] in self.__terminator or expression[symbol_index] == e:
                    break
                index_symbol_has_null = self.__is_in_null_list(expression[symbol_index])
                if index_symbol_has_null and symbol_index != len(expression) - 1:
                    continue
                elif not index_symbol_has_null:
                    break
                else:
                    return True
        return False

    def __make_null_list(self):
        for e in self.__firstChild:
            if self.__is_in_null_list(e):
                self.__hasNULL.append(e)
        self.__hasNULL = list(set(self.__hasNULL))

    def get_first(self):
        if not self.__haveMadeFirst:
            self.__make_null_list()
            for e in self.__firstChild:
                self.__calculate_first(e)
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

    def get_first_of(self, expression):
        first = list()
        for symbol_index in range(len(expression)):
            if expression[symbol_index] in self.__terminator:
                first.append(expression[symbol_index])
                return first
            elif expression[symbol_index] == '$':
                first.append('$')
                return first
            for tmp in self.__firstSet[expression[symbol_index]]:
                if tmp != 'ε':
                    first.append(tmp)
            if expression[symbol_index] in self.__hasNULL:
                continue
            else:
                break
        return first

    def __update_follow_set(self):
        for father in self.__record:
            for child in self.__record[father]:
                self.__followSet[child] += self.__followSet[father]
                self.__followSet[child] = list(set(self.__followSet[child]))
        for e in self.__followSet:
            self.__followSet[e] = list(set(self.__followSet[e]))
        return

    def __calculate_first(self, e):
        for expression in self.__firstChild[e]:
            for tmpSymbolIndex in range(len(expression)):
                if expression[tmpSymbolIndex] in self.__terminator:
                    self.__firstSet[e].append(expression[tmpSymbolIndex])
                    self.__update_first_set()
                    break
                elif expression[tmpSymbolIndex] == e:
                    if tmpSymbolIndex != len(expression) - 1 and e in self.__hasNULL:
                        self.__firstChild[e].append(expression[1:])
                    break
                self.__record[expression[tmpSymbolIndex]].append(e)
                self.__update_first_set()
                if expression[tmpSymbolIndex] not in self.__hasNULL:
                    break
