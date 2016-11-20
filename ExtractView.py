#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import csv
import numpy
import json
import jieba
import jieba.posseg
import sys
import jieba
import  numpy as np
import re
# TODO结束后搜索L和T进行处理，搜索空格进行处理，搜索-进行处理,字母结尾的要审核"北京E",有可能是连续的,中间没能识别，断了；单数字和字母
# 单独抽数字和字母，做字典    #有可能多款车型在一起

extraCars = ["尼桑", "野帝", "哈佛", "荣放", "凌度", "凌渡", "上海通用", "凌志", "速腾r-line", "速腾gli", "高尔夫gti", "奔弛",
             "马自达全球", "启程","逸杰", "普桑", "高尔夫7", "crosspolo", "cross polo", "cross", "polo", "神龙汽车", "神龙"]
endOneNames = ["京", "型", "团", "厂", "站", "省", "街","市", "区", "国", "级", "集", "路", "版", "店", "式", "网", "感", "化", "款"]
endTwoNames = ["北京", "厂商","mm", "功能", "地区", "上海", "南京", "陕西", "重庆", "中华", "总裁"]

def find_lcsubstr(s1, s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]  #生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax=0   #最长匹配的长度
    p=0  #最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
                    p=i+1
    return s1[p-mmax:p]   #返回最长子串及其长度


def find_lcseque(s1, s2):
    # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
    m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
    # d用来记录转移方向
    d = [[None for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:  # 字符匹配成功，则该位置的值为左上方的值加1
                m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                d[p1 + 1][p2 + 1] = 'ok'
            elif m[p1 + 1][p2] > m[p1][p2 + 1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                d[p1 + 1][p2 + 1] = 'left'
            else:  # 上值大于左值，则该位置的值为上值，并标记方向up
                m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                d[p1 + 1][p2 + 1] = 'up'
    (p1, p2) = (len(s1), len(s2))
    # print(numpy.array(d)
    s = []
    while m[p1][p2]:  # 不为None时
        c = d[p1][p2]
        if c == 'ok':  # 匹配成功，插入该字符，并向左上角找下一个
            s.append(s1[p1 - 1])
            p1 -= 1
            p2 -= 1
        if c == 'left':  # 根据标记，向左找下一个
            p2 -= 1
        if c == 'up':  # 根据标记，向上找下一个
            p1 -= 1
    s.reverse()
    return ''.join(s)

# def isValidWord(cartype, word):

def isAlpha(w):
    if (w >= 'a' and w <= 'z') or (w >= 'A' and w <= 'z'):
        return True
    return False

def isNum(w):
    if w >= '0' and w <= '9':
        return True
    return False


def onlyDigAlpha(word):
    for i in np.arange(len(word) - 1, -1, -1):
        if not (isAlpha(word[i]) or isNum(word[i])):
            return False
    return True


def endWithDigAlpha(word):
    if isAlpha(word[-1]):
        return True
    if isNum(word[-1]):
        return True
    return False

def lenOfEng(word):
    res = 0
    for i in np.arange(len(word) - 1, -1, -1):
        if isAlpha(word[i]) or isNum(word[i]):
            res += 1
        else:
            break
    return res

def delPostfix(word):
    res = word
    flag = True
    while(res.__len__() >= 2 and flag):
        if(res[-2] + res[-1]) in ["集团", "汽车","公司","客车","火车"]:
            res = res[0:res.__len__() - 2:1]
            flag = True
        elif res[-1] in ["车", "厂","^","-"]:
            res = res[0:res.__len__() - 1:1]
            flag = True
        else:
            flag = False
    return res


if __name__ == "__main__":
    # encoding=utf-8
    base_path = "/home/jun/Desktop/contest/sentimentAnalysis/"
    # hello = ["hh", "88","faskf"]
    # print(hello[-1:-3:-1])
    # f = open(base_path + "cars.json")
    # data = json.load(f)
    # # print (data)
    # f.close()
    # cartype = {}
    # user_dict = open(base_path + 'user.dict', 'w')
    # for sample in data:
    #     cartype[sample["company"].strip().replace(" ", "").replace(".", "").lower()] = True
    #     cartype[sample["brand"].strip().replace(" ","").replace(".","").lower()] = True
    #     cartype[sample["line"].strip().replace(" ","").replace(".","").lower()] = True
    # user_dict = open(base_path + 'user.dict', 'w')
    # for element in cartype.keys():
    #     print(element, " ", "3", file=user_dict)
    # print("上汽大众", " ", "1000000" "n", file=user_dict)
    #
    # user_dict.close()
    # print(cartype)
    # print(cartype.__len__())


            # print(" ".join(seg_list))
    # print("")
    #
    # seg_list = jieba.cut_for_search(sentence)  # 搜索引擎模式
    # print(", ".join(seg_list))

    cartype = {}
    # f = open(base_path + "cars.json")
    # data = json.load(f)
    # f.close()

    user_dict = open(base_path + 'user.dict', 'r')
    for line in user_dict:
        sentence = list(line.strip().split(" "))[0].strip().replace(".", "")
        cartype[sentence] = True
    user_dict.close()
    print(cartype.keys())
    print(cartype.keys().__len__())

    # for sample in data:
    #     cartype[sample["company"].strip().replace(" ", "^").replace(".", "").replace("-","").lower()] = True
    #     cartype[sample["brand"].strip().replace(" ","^").replace(".","").replace("-","").lower()] = True
    #     cartype[sample["line"].strip().replace(" ","^").replace(".","").replace("-","").lower()] = True
    # print(cartype)
    # print(cartype.__len__())


    # for car in extraCars:
    #     cartype[car] = True


    csvfile = open('Test.csv', 'r')
    # # print(csvfile)
    # user_dict = open(base_path + 'user.dict1', 'w')
    # # for element in cartype.keys():
    # #     print(element, " ", "3", file=user_dict)
    # for line in csvfile:
    #     sentence = list(line.strip().split('\t'))[1].strip().replace(" ","^")
    #     # rowNum = list(line.strip().split('\t'))[0].strip()
    #     print(sentence," ", "100 ","n", file= user_dict)
    #
    # for element in cartype.keys():
    #     print(element, " ", "100", file=user_dict)
    #
    # user_dict.close()
    info = []
    correct = 0
    i = 0

    carleft1 = []
    sentenceDict = {}

    # print(find_lcseque("施小军", "施军你好"))
    #
    # sentence ="因为我们刚刚从工信部燃料消耗信息网上得知，上汽大众全新途观保留手动挡车型，就是说全新途观还是有保留入门版的车型，价格可能会贵，但起码有个低门槛的在，不像上次上市的新款RAV4 荣放，直接取消了手动挡。"

    # seg_list = jieba.cut(sentence, cut_all=True)

    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    #
    # seg_list = jieba.cut(sentence, cut_all=False)
    # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    #
    # seg_list = jieba.cut(sentence)  # 默认是精确模式
    # for w in seg_list:
    #     print(w.word, w.flag)

    #
    # l = []
    # for i in seg:
    #     l.append((i.word, i.flag))
    # for element in l:
    #     print(element[0], element[1])
    # testRes = open(base_path + 'testRes.txt', 'w')
    # testRes = open("stdout", 'w')
    # print(cartype.keys())
    jieba.load_userdict(base_path + "user.dict")

    # sentence = "速腾R-Line, 一汽-大众"
    # sentence = sentence.strip().lower()
    # string = sentence.strip()
    # seg = jieba.posseg.cut(string)
    # for w in seg:
    #     print(w.word, "", w.flag)
    # print(cartype.keys())

    years = np.arange(1000,2020,1)
    uselessWordsDict = {}
    uselessWords = ["全新", "运动","运动感","原型车","小汽车", "风景", "进口车","电动汽车",
                    "华晨集团", "概念车", "发现", "概念", "车", "店", "元", "行车","TSI","现代五项",
                    "货车","电动车","多","功能","丰富","新能源","制造商","自行车集","进口","电动车窗",
                    "汽车品牌","品牌","制造","led","中国女排","汽车网","制造理念","理念","L","风景线",
                    "新闻", "汽车新闻","mm","中国制造","成功人士","汽车集团","城市道路","制造业","面包车","澳大利亚",
                    "货车", "拖车", "公车", "计程车", "露营车","里程", "轿车", "厢型车","掀背车", "斜背车","电动机",
                    "卡车", "韩国", "中国", "经典", "电动", "集团","全球","风尚","总裁","变形金刚","韩国大宇",
                    "旅行车","高级车","中级车", "得意", "国民车","越野车", "商务车", "多功能", "休旅车","厢式",
                    "休旅车","跑车","成功","经验","mod", "城市","道路","集团","4S","优雅","里程碑","CD机","客车",
                    "敞篷车","超级", "年", "小型车", "中型车","汽车论坛", "大型车","自行车","旅行车","运动版","中华世纪坛",
                    "4s店", "4s", "mpv", "MPV", "pro","PRO", "suv", "SUV", "功能丰富","级车","型车","篷车","重庆",
                    "一","二","三","四","五","六","七", "八","九","8888",")","(","副总裁"]

    validflag = ["n", "eng", "m", "nrt", "ns","nrfg", "nt", "x","nz", "nr", "v", "z", "j"]
    validflagDict = {}
    for flag in validflag:
        validflagDict[flag] = True

    uselessWords = np.concatenate((years, uselessWords))
    for word in uselessWords:
        uselessWordsDict[word] = True
    # print(uselessWords )
    # print(cartype)
    feedback = {}
    for line in csvfile:
        # info.append(list(line.strip().split('\t'))[1])
        # print(info)
        # print(line)
        i += 1
        sentence = list(line.strip().split('\t'))[1].strip().replace(" ","^").replace(".","8888").replace("--","8888").replace("DSG", "8888")
        rowNum = list(line.strip().split('\t'))[0].strip()
        feedback[rowNum] = sentence
        # if(rowNum == "028109"):
        #     print(sentence)
        string = sentence.strip()
        # print(sentence)
        seg = jieba.posseg.cut(string)
        prevword = ""
        sentenceDict[rowNum] = {}
        justNum = False
        justAlpha = False

        # print (type(seg))
        # print(rowNum)
        prevDash = False
        # for word in seg:
        #     # if(rowNum == "027446"):
        #     print(word.word, word.flag)

        for word in seg:
            # if(rowNum == "027446"):
            # print(word.word, word.flag)
            # print((word.word.lower()[-4:-1:1] + word.word.lower()[-1]))
            # num2016 = False
            # if (word.word.lower().__len__() >= 4):
            #     last4words = (word.word.lower()[-4:-1:1] + word.word.lower()[-1])
            #     print(last4words)
            #     if last4words in years:
            #         num201
            # 6 = True
            # print(num2016)
            if uselessWordsDict.__contains__(word.word.lower()) or (not validflagDict.__contains__(word.flag) and  word.word.lower() != "明锐"):

                # if(prevword.replace("-","").lower() != ""):
                #     if not sentenceDict[rowNum].__contains__(prevword.replace("-","").lower()):
                #         sentenceDict[rowNum][prevword.replace("-","").lower()] = True
                #         print(rowNum, " ", prevword.replace("-","").lower())
                #         prevword.replace("-","").lower() = ""
                if (prevword.replace("-","").lower() != ""):
                    prevword = delPostfix(prevword)
                    if(prevword == ""):
                        continue
                    flag1 = False
                    if (justAlpha):
                        if (prevword.replace("-","").lower().__len__() >= 2):
                            for key in cartype.keys():
                                if find_lcsubstr(key, prevword.replace("-","").lower()).__len__() == prevword.replace("-","").lower().__len__():
                                    if (key[-1] == prevword.replace("-", "").lower()[-1] and lenOfEng(
                                            key) == prevword.replace("-", "").lower().__len__()):
                                        flag1 = True
                    elif justNum:
                        # flag1 = False
                        if (prevword.replace("-","").lower().__len__() > 2):
                            for key in cartype.keys():
                                if find_lcsubstr(key, prevword.replace("-","").lower()).__len__() == prevword.replace("-","").lower().__len__():
                                    if (key[-1] == prevword.replace("-","").lower()[-1]and prevword.replace("-","").lower()[-1:-3:-1] != "00"):
                                        flag1 = True
                    else:
                        flag1 = True
                    if flag1:
                        if not sentenceDict[rowNum].__contains__(prevword.replace("-","").lower()):
                            if (prevword.replace("-","").lower()[-1] not in endOneNames):
                                if(prevword.replace("-","").lower().__len__() >=2 and (prevword.replace("-","").lower()[-2] + prevword.replace("-","").lower()[-1]) not in endTwoNames) or prevword.replace("-","").lower().__len__() == 1:
                                    sentenceDict[rowNum][prevword] = True
                                    # print(rowNum, " ", prevword.replace("-","").lower(), file=testRes)
                                    print(rowNum, " ", prevword)
                prevword = ""
                justAlpha = False
                justNum = False
                # if(prevword.replace("-","").lower() != ""):
                #     print(prevword.replace("-","").lower())
                # prevword.replace("-","").lower() = ""
                continue
            # if (seg.__ge__(word) == "元"):
            #     continue
            if word.word.lower() == "^":
                if (prevword.replace("-","").lower() != ""):
                    prevword = prevword + word.word
                    # print("hello", prevword.replace("-","").lower())
                continue
            if word.word.lower() == "-":
                if (prevword.replace("-","").lower() != ""):
                    prevword = prevword + word.word
                    prevDash = True
                    # print("hello", prevword.replace("-","").lower())
                continue

            isCar = False
            if  cartype.__contains__(word.word.lower()) or prevDash:
                isCar = True
                justNum = False
                justAlpha = False
            else:
                for key in cartype.keys():
                        if word.flag == "eng" and (prevword.replace("-","").lower() == "" or justAlpha):
                            if find_lcsubstr(key, word.word.lower()) == word.word.lower():
                                if prevword.replace("-", "").lower() != "" and find_lcsubstr(key, (
                                            prevword + word.word.lower()\
                                        ).replace("-","").lower()).__len__() == (float)(prevword.replace("-", "").lower().__len__() + word.word.__len__()):
                                    justAlpha = True
                                    isCar = True
                                    break
                        elif(word.flag == "m" and (prevword.replace("-","").lower() == "" or justNum)):
                            if find_lcsubstr(key, word.word.lower()) == word.word.lower():
                                if prevword.replace("-", "").lower() != "" and find_lcsubstr(key, (
                                    prevword + word.word.lower()).replace("-",
                                                                          "").lower()).__len__() == \
                                        (float)(prevword.replace("-", "").lower().__len__() + word.word.__len__()):
                                    justNum = True
                                    isCar = True
                                # print("aaa", word.word.lower(), justNum)
                                break
                        elif (word.flag == "m" or "x" or "eng") and find_lcsubstr(key, word.word.lower()) == word.word.lower():
                            if (prevword.replace("-", "").lower() != "" and find_lcsubstr(key, (prevword + word.word.lower()).replace("-",
                                 "").lower()).__len__() >= (float)(2.0 / 3.0 *(prevword.replace("-", "").lower().__len__() + word.word.__len__()))):
                                # print(key)
                                justAlpha = False
                                justNum = False
                                isCar = True
                                break
                        else:
                            if find_lcsubstr(key, word.word.lower()).__len__() >= 2:
                                if (prevword.replace("-","").lower() != "" and find_lcsubstr(key, (prevword + word.word.lower()).replace("-",
                                    "").lower()).__len__() > word.word.__len__() ) \
                                    or (prevword.replace("-","").lower() == "" and
                                            (float)(find_lcsubstr(key, word.word.lower()).__len__()) \
                                        >= (float)(2.0 /3.0 *(prevword.replace("-", "").lower().__len__() + word.word.__len__())):
                                    justAlpha = False
                                    justNum = False
                                    isCar = True
                                    break
            if isCar:
                    prevword = prevword + word.word
                    prevDash = False
            else:
                if(prevword != "汽车" and prevword.replace("-","").lower() != ""):
                    prevword = delPostfix(prevword)
                    if (prevword == ""):
                        continue
                    flag1 = False
                    if justAlpha:
                        if(prevword.replace("-","").lower().__len__() >= 2):
                            for key in cartype.keys():
                                if find_lcsubstr(key, prevword.replace("-","").lower()).__len__() == prevword.replace("-","").lower().__len__():
                                    if (key[-1] == prevword.replace("-", "").lower()[-1] and lenOfEng(
                                            key) == prevword.replace("-", "").lower().__len__()):
                                        flag1 = True
                                    # print("wodetian",prevword.replace("-","").lower())
                    elif justNum:
                        # flag1 = False
                        if (prevword.replace("-","").lower().__len__() > 2):
                            for key in cartype.keys():
                                if find_lcsubstr(key, prevword.replace("-","").lower()).__len__() == prevword.replace("-","").lower().__len__():
                                    if (key[-1] == prevword.replace("-","").lower()[-1] and prevword.replace("-","").lower()[-1:-3:-1] != "00"):
                                        flag1 = True
                    else:
                        flag1 = True
                    if flag1:
                        if not sentenceDict[rowNum].__contains__(prevword.replace("-","").lower()) :
                            if (prevword.replace("-","").lower()[-1] not in endOneNames):
                                if(prevword.replace("-","").lower().__len__() >=2 and (prevword.replace("-","").lower()[-2] + prevword.replace("-","").lower()[-1]) not in endTwoNames) or prevword.replace("-","").lower().__len__()==1:
                                    sentenceDict[rowNum][prevword] = True
                                    # print(rowNum, " ", prevword.replace("-","").lower(), file=testRes)
                                    print(rowNum, " ", prevword)
                prevword = ""
                justAlpha = False
                justNum = False

        if(prevword != "汽车" and prevword.replace("-","").lower() != ""):
            prevword = delPostfix(prevword)
            if (prevword == ""):
                continue
            flag1 = False
            if justAlpha:
                if (prevword.replace("-", "").lower().__len__() >= 2):
                    for key in cartype.keys():
                        if find_lcsubstr(key, prevword.replace("-", "").lower()).__len__() == prevword.replace("-",
                                "").lower().__len__():
                            if (key[-1] == prevword.replace("-", "").lower()[-1] and lenOfEng(key) == prevword.replace("-", "").lower().__len__()):
                                flag1 = True

            elif justNum:
                # flag1 = False
                if (prevword.replace("-", "").lower().__len__() > 2):
                    for key in cartype.keys():
                        if find_lcsubstr(key, prevword.replace("-", "").lower()).__len__() == prevword.replace("-",
                            "").lower().__len__():
                            if (key[-1] == prevword.replace("-", "").lower()[-1] and prevword.replace("-", "").lower()[-1:-3:-1] != "00"):
                                flag1 = True
            else:
                flag1 = True
            if flag1:
                if (not sentenceDict[rowNum].__contains__(prevword.replace("-","").lower())):
                    if (prevword.replace("-","").lower()[-1] not in endOneNames):
                        if (prevword.replace("-","").lower().__len__() >= 2 and (prevword.replace("-","").lower()[-2] + prevword.replace("-","").lower()[-1]) not in endTwoNames) or prevword.replace("-","").lower().__len__() == 1:
                            sentenceDict[rowNum][prevword] = True
                            # print(rowNum, " ", prevword.replace("-","").lower(), file=testRes)
                            print(rowNum, " ", prevword)
        prevword = ""
        justAlpha = False
        justNum = False

    # print("===============================================")
    # print("===============================================")
    # print("===============================================")

    DA = {}
    EDA = {}
    OL6 = {}
    Others = {}
    Emp = {}
    ONE = {}

    for rowNum in sentenceDict.keys():
        # print(i, sentenceDict[i], file=testRes)
        if sentenceDict[rowNum].keys().__len__() != 0:
            put = False
            for val in sentenceDict[rowNum].keys():
                if val.__len__() == 1:
                    ONE[rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif onlyDigAlpha(val):
                    DA[rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif endWithDigAlpha(val):
                    EDA[rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif val.__len__() >= 6:
                    OL6[rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                else:
                    continue

            if not put:
                Others[rowNum] = list(sentenceDict[rowNum].keys())
        else:
            Emp[rowNum] = []

    output = open(base_path + 'testres3', 'w')
    print("ONE=============================================", file=output)
    for i in ONE.keys():
        print(i, ONE[i], file=output)


    print("DA=============================================", file=output)
    for i in DA.keys():
        print(i, DA[i], file=output)


    print("EDA=============================================", file=output)
    for i in EDA.keys():
        print(i, EDA[i], file=output)

    print("OL6=============================================", file=output)
    for i in OL6.keys():
        print(i, OL6[i], file=output)

    print("Others=============================================", file=output)
    for i in Others.keys():
        print(i, Others[i], file=output)

    print("EMP=============================================", file=output)
    for i in Emp.keys():
        print(i, Emp[i], file=output)

    print("EMPSentence=============================================", file=output)
    for i in Emp.keys():
        print(i, feedback[i], file=output)
    output.close()



    output = open(base_path + 'testres3-1', 'w')
    print("ONE=============================================", file=output)
    for i in ONE.keys():
        print(i, ONE[i], file=output)
        print(i, feedback[i], file=output)

    print("DA=============================================", file=output)
    for i in DA.keys():
        print(i, DA[i], file=output)
        print(i, feedback[i], file=output)

    print("EDA=============================================", file=output)
    for i in EDA.keys():
        print(i, EDA[i], file=output)
        print(i, feedback[i], file=output)

    print("OL6=============================================", file=output)
    for i in OL6.keys():
        print(i, OL6[i], file=output)
        print(i, feedback[i], file=output)

    print("Others=============================================", file=output)
    for i in Others.keys():
        print(i, Others[i], file=output)
        print(i, feedback[i], file=output)

    print("EMP=============================================", file=output)
    for i in Emp.keys():
        print(i, Emp[i], file=output)
        print(i, feedback[i], file=output)

    print("EMPSentence=============================================", file=output)
    for i in Emp.keys():
        print(i, feedback[i], file=output)
        print(i, feedback[i], file=output)
    output.close()



    # print('东风悦达起亚'.__len__())
    # print(endWithDigAlpha('标致505'))


        # print(i, sentenceDict[i].keys())

    # testRes.close()
    # prev = correct / i
    #
    #
    #
    # carleft2 = []
    # for car in carleft1:
    #     flag = False
    #     for key in cartype.keys():
    #         if find_lcseque(key, car).__len__() >= 3:
    #             correct += 1
    #             flag = True
    #             break
    #     if not flag:
    #         carleft2.append(car)
    #
    # print(prev)
    # print(carleft2.__len__())
    # print(carleft2)
    # print(correct / i)
    #
    # extraDict =["凌渡", ""]
    # # cartype[] =

















# from __future__ import print_function, unicode_literals
# import jieba
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))
#
#
# #encoding=utf-8
#
# import sys
# sys.path.append("../")
# import jieba
# # jieba.load_userdict("userdict.txt")
# import jieba.posseg as pseg
#
# jieba.add_word('石墨烯')
# jieba.add_word('凱特琳')
# jieba.del_word('自定义词')
#
# test_sent = (
# "李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
# "例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
# "「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
# )
# words = jieba.cut(test_sent)
# print('/'.join(words))
#
# print("="*40)
#
# result = pseg.cut(test_sent)
#
# for w in result:
#     print(w.word, "/", w.flag, ", ", end=' ')
#
# print("\n" + "="*40)
#
# terms = jieba.cut('easy_install is great')
# print('/'.join(terms))
# terms = jieba.cut('python 的正则表达式是好用的')
# print('/'.join(terms))
#
# print("="*40)
# # test frequency tune
# testlist = [
# ('今天天气不错', ('今天', '天气')),
# ('如果放到post中将出错。', ('中', '将')),
# ('我们中出了一个叛徒', ('中', '出')),
# ]
#
# for sent, seg in testlist:
#     print('/'.join(jieba.cut(sent, HMM=False)))
#     word = ''.join(seg)
#     print('%s Before: %s, After: %s' % (word, jieba.get_FREQ(word), jieba.suggest_freq(seg, True)))
#     print('/'.join(jieba.cut(sent, HMM=False)))
#     print("-"*40)
#
#
