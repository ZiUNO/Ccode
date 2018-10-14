# 编译原理上机代码
### Grammatical analysis
###### main
    主函数对集合进行初始化、赋值和LL（1）文法创建
### lib
###### FFSet
    创建集合并计算First集和Follow集
###### LL1
    传入集合（满足LL（1）），计算预测分析表，检测传入语句是否满足该文法
### src
    FFSet读取该路径下的指定文件初始化集合