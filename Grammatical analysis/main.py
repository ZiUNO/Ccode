# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Contact: github.com/ZiUNO/Compile-Code
* @Software: PyCharm
* @Time: 2018/10/14 14:30
"""

from lib.FFSet import FFSet
from lib.LL1 import LL1

# fileName = input("Grammar file name:")
fileName = 'test.txt'
f = open("../src/" + fileName)
size = int(f.readline())  # 非终结符个数
ffset = FFSet(size)
terminator = f.readline().strip().split(" ")  # 所有的终结符
ffset.setTermi(terminator)
for i in range(size):
    grammarLine = f.readline().strip()
    e = grammarLine.split("->")[0]
    expression = grammarLine.split("->")[1]
    ffset.inputGrammar(e, expression)
    if i == 0:
        ffset.setFirstNontermi(e)
    elif i == size - 1:
        ffset.setLastNontermi(e)
f.close()
print("终结符：", ffset.getTermi())
print("文法:", ffset.getGrammar())
print("First集:", ffset.getFirst())
print("Follow集:", ffset.getFollow())
grammarAnalysis = LL1(ffset)
print(grammarAnalysis.getChart())
# toCheck = input("输入语句（以$结尾）：")
toCheck = '+d*+d$'
process, message = grammarAnalysis.check(toCheck)
print(process)
print(message)