# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/26 20:08
"""


class LR1:
    ROOT = '#R'
    ACC = 'ACC'
    ERROR_UNEXPECTED = 'UE'
    ERROR_MISSING = 'MI'
    ACTION = {
        's': '移进',
        'r': '归约'
    }

    def __init__(self, ffset):
        self.__ffset = ffset
        self.__grammar = ffset.get_grammar()
        self.__terminators = ffset.get_terminator_of_follow()
        self.__formula = self.__make_formula()
        self.__items = list()
        self.__lr_map = list()
        LR1.__get_item_index_of(self.__items, [[LR1.ROOT, '', ffset.get_first_non_terminator(), ['$']]])
        self.__make_items()
        del self.__ffset
        del self.__grammar

    def get_items(self):
        return self.__items

    def get_lr_map(self):
        return self.__lr_map

    @staticmethod
    def __get_item_index_of(items, item):
        for tmp_item_index in range(len(items)):
            if sorted(items[tmp_item_index]) == sorted(item):
                return tmp_item_index
        else:
            item_to_append = item.copy()
            for index_in_item in range(len(item_to_append)):
                item_to_append[index_in_item][-1] = sorted(list(set(item_to_append[index_in_item][-1])))
            items.append(item_to_append)
            return len(items) - 1

    def __make_items(self):
        for item_set in self.__items:
            new_item_map = {}
            for terminator in self.__terminators:
                new_item_map[terminator] = None
            for non_terminator in self.__grammar:
                new_item_map[non_terminator] = None
            item_set_num = LR1.__get_item_index_of(self.__items, item_set)
            self.__make_closure(item_set)
            self.__items[item_set_num] = item_set
            new_items = []
            for item in item_set:
                father = item[0]
                backward = item[1]
                forward = item[2]
                search_operators = item[3]
                if len(forward) == 0:
                    if father == LR1.ROOT:
                        new_item_map['$'] = LR1.ACC
                    else:
                        index_of_reduction = self.__formula.index([father, backward])
                        for search_operator in search_operators:
                            new_item_map[search_operator] = 'r%s' % index_of_reduction
                else:
                    expect_symbol = forward[0]
                    backward += expect_symbol
                    forward = forward[1:]
                    next_item_set = [[father, backward, forward, search_operators]]
                    self.__make_closure(next_item_set)
                    state = new_item_map[expect_symbol]
                    if state is None:
                        next_item_index = LR1.__get_item_index_of(new_items, next_item_set)
                        if expect_symbol in self.__terminators:
                            new_item_map[expect_symbol] = 's%d' % next_item_index
                        else:
                            new_item_map[expect_symbol] = '%d' % next_item_index
                    else:
                        if state[0] == 's':
                            next_item_index = int(state[1:])
                        else:
                            next_item_index = int(state)
                        new_items[next_item_index] += next_item_set
            for non_terminator in self.__grammar:
                state = new_item_map[non_terminator]
                if state is None:
                    continue
                else:
                    state = int(state)
                    item_index = LR1.__get_item_index_of(self.__items, new_items[state])
                    new_item_map[non_terminator] = item_index
            for terminator in self.__terminators:
                state = new_item_map[terminator]
                if state is None:
                    new_item_map[terminator] = LR1.ERROR_UNEXPECTED
                    continue
                elif state[0] == 's':
                    item_index = LR1.__get_item_index_of(self.__items, new_items[int(state[1:])])
                    new_item_map[terminator] = 's%d' % item_index
            self.__lr_map.append(new_item_map)

    def check(self, to_check):
        process = []
        message = []
        count_error = 0
        to_check = list(reversed(to_check))
        if to_check[0] != '$':
            to_check.insert(0, '$')
        stack = [0]
        column_count = 0
        separator = '\n'
        while len(to_check) != 0:
            tmp_to_check = to_check.pop()
            top = stack[-1]
            state = self.__lr_map[top][tmp_to_check]
            column_count += 1
            if state == LR1.ERROR_UNEXPECTED:
                process_to_append = 'error'
                count_error += 1
                message_to_append = '[ERROR(No.%d)]unexpected %s at %d column' % (
                    count_error, tmp_to_check, column_count)
                missing = []
                for terminator in self.__terminators:
                    state = self.__lr_map[top][terminator]
                    if state == LR1.ERROR_UNEXPECTED:
                        continue
                    elif state[0] == 's':
                        missing.append(terminator)
                if len(missing) == 0:
                    missing = ''
                else:
                    missing = "(maybe missing '%s')" % "'or'".join(missing)
                message.append(message_to_append + missing)
            elif state[0] == 's':
                next_item_index = int(state[1:])
                stack.append(tmp_to_check)
                stack.append(next_item_index)
                process_to_append = LR1.ACTION['s']
            elif state[0] == 'r':
                e, production = self.__formula[int(state[1:])]
                production_len = len(production)
                for tmp in range(production_len):
                    stack.pop()
                    stack.pop()
                after_r_state = stack[-1]
                stack.append(e)
                stack.append(self.__lr_map[after_r_state][e])
                process_to_append = '按照%s->%s归约' % (e, production)
                to_check.append(tmp_to_check)
                column_count -= 1
            else:
                process_to_append = '接受'
            process.append(process_to_append)
        tail_message = 'total %d error(s)' % len(message)
        message.append(tail_message)
        return separator.join(process), separator.join(message)

    def __make_closure(self, item):
        for expression in item:
            forward = expression[2]
            if len(forward) == 0 or forward[0] in self.__terminators:
                continue
            else:
                e = forward[0]
                for production in self.__grammar[e]:
                    first_of_tail = list()
                    for tail in expression[3]:
                        first_of_tail += self.__ffset.get_first_of(forward[1:] + tail)
                    first_of_tail = sorted(list(set(first_of_tail)))
                    item_to_append = [e, '', production, first_of_tail]
                    for tmp_item_index in range(len(item)):
                        if item[tmp_item_index][0:3] == item_to_append[0:3]:
                            item[tmp_item_index][3] += item_to_append[3]
                            item[tmp_item_index][3] = sorted(list(set(item[tmp_item_index][3])))
                            break
                    else:
                        item.append(item_to_append)

    def __make_formula(self):
        formula = list()
        for e in self.__grammar:
            for expression in self.__grammar[e]:
                formula.append([e, expression])
        return formula
