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
import pickle
import pypinyin
# TODO结束后搜索L和T进行处理，搜索空格进行处理，搜索-进行处理,字母结尾的要审核"北京E",有可能是连续的,中间没能识别，断了；单数字和字母
# 单独抽数字和字母，做字典    #有可能多款车型在一起

extraCars = ["尼桑", "幻速", "小宝","大宝", "野帝", "哈佛", "荣放", "凌度", "凌渡", "上海通用", "凌志", "速腾r-line", "速腾gli", "高尔夫gti", "奔弛",
             "马自达全球", "启程","逸杰", "普桑", "高尔夫7", "crosspolo", "cross polo", "cross", "polo", "神龙汽车", "神龙"]
endOneNames = ["京", "型", "团", "厂", "站", "省", "街","市", "区", "国", "级", "集", "路", "版", "店", "式", "网", "感", "化", "款"]
endTwoNames = ["北京","集团", "厂商","mm", "功能", "地区", "上海", "南京", "陕西", "重庆", "中华", "总裁"]
oneNameCars = ["秦", "宋"]
uselessWords = ["“", "”", "全新", "运动", "运动感", "原型车", "小汽车", "风景", "进口车", "电动汽车",
                "集团", "概念车", "发现", "概念", "车", "店", "元", "行车", "TSI", "现代五项",
                "货车", "电动车", "多", "功能", "丰富", "新能源", "制造商", "自行车集", "进口", "电动车窗",
                "汽车品牌", "品牌", "制造", "led", "中国女排", "汽车网", "制造理念", "理念", "L", "风景线",
                "新闻", "汽车新闻", "中华民族", "mm", "中国制造", "成功人士", "汽车集团", "城市道路", "制造业", "面包车", "澳大利亚",
                "货车", "拖车", "公车", "计程车", "露营车", "里程", "轿车", "厢型车", "掀背车", "斜背车", "电动机",
                "卡车", "韩国", "中国", "经典", "电动", "集团", "全球", "风尚", "总裁", "变形金刚", "韩国大宇",
                "旅行车", "高级车", "中级车", "得意", "国民车", "越野车", "商务车", "多功能", "休旅车", "厢式",
                "休旅车", "跑车", "成功", "经验", "mod", "城市", "道路", "集团", "4S", "优雅", "里程碑", "CD机", "客车",
                "敞篷车", "超级", "年", "小型车", "中型车", "汽车论坛", "大型车", "自行车", "旅行车", "运动版", "中华世纪坛",
                "4s店", "4s", "mpv", "MPV", "pro", "PRO", "suv", "SUV", "功能丰富", "级车", "型车", "篷车", "重庆",
                "一", "二", "三", "四", "五", "六", "七", "八", "九", "8888", ")", "(", "副总裁","北京","集团", "厂商","mm", "功能", "地区", "上海", "南京", "陕西", "重庆", "中华", "总裁"]
numeber_cars = ["330", "45", "280", "301", "280","301","307","308",
"320","323","328","330","350","380","408","500","508","525","820","2008","3008","4008","5008"]

def find_lcsubstr(s1, s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]  #生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax=0   #最长匹配的长度
    p=0  #最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            flag = False
            if s1[i] == s2[j]:
                flag = True
            # else:
            #     if emission_mat.__contains__(s1[i]) and emission_mat.__contains__(s2[j]):
            #         for pinyin in emission_mat[s1[i]]:
            #             if flag:
            #                 break
            #             for pinyin2 in emission_mat[s2[j]]:
            #                 if pinyin == pinyin2:
            #                     flag = True
            #                     break
            if flag:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1] > mmax:
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
    # #print(numpy.array(d)
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
    if (w >= 'a' and w <= 'z') or (w >= 'A' and w <= 'Z'):
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

def onlyDig(word):
    for i in np.arange(0, len(word), 1):
        if not (isNum(word[i])):
            return False
    return True

def onlyAlpha(word):
    for i in np.arange(0, len(word), 1):
        if not (isAlpha(word[i])):
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


def suffix_match(word1, word2):
    if word1[0] == word2[0] or word1[-1] == word2[-1]:
        return True
    return False


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

def output(prevword, isCar, word, sentenceDict, rowNum, cartype):
    prevword = delPostfix(prevword)
    is_valid= False
    prevword1 = prevword.replace("-","").lower().strip()
    len1 = prevword1.__len__()
    if prevword1 not in uselessWords:
        if prevword1.__len__() <=1:
            if prevword1 != "" and prevword1 in oneNameCars:
                is_valid = True
        elif onlyDig(prevword1):
            if prevword1 in numeber_cars:
                is_valid = True
        elif onlyAlpha(prevword1):
            #print("I am here")
            for key in cartype.keys():
                if find_lcsubstr(key, prevword1).__len__() == len1:
                    #print(prevword1,key)
                    if (key[-1] == prevword1[-1] and lenOfEng(key) == len1):
                        is_valid = True
        elif onlyDigAlpha(prevword1):
            for key in cartype.keys():
                if find_lcsubstr(key, prevword1).__len__() == len1:
                    # print(prevword1,key)
                    if (key[-1] == prevword1[-1] and lenOfEng(key) == len1):
                        is_valid = True
        else:
            for key in cartype.keys():
                lcs = find_lcsubstr(key, prevword1)
                tmp_len = lcs.__len__()
                # # print(pypinyin.lazy_pinyin(lcs) == pypinyin.lazy_pinyin(prevword1)
                # if (key.__len__() == tmp_len and (float)(len1 * 3.0 / 4.0) <= key.__len__()) or (tmp_len == len1 and (float)(key.__len__() * 2.0 / 3.0) <= len1)\
                #         or (find_lcseque(key, prevword1).__len__() >= 4):
                #     #suffix_match(key, prevword1) and
                #     is_valid = True
                #     break
    if is_valid:
        prevword = prevword.strip().lstrip("-").rstrip("-")
        if not sentenceDict[rowNum].__contains__(prevword):
                    sentenceDict[rowNum][prevword] = True
                    print(rowNum, " ", prevword)
    if isCar:
        prevword = word.word
    else:
        prevword = ""
    return prevword, sentenceDict


def classify_output(res, feedback):
        output1 = open("classify_res_no_sentence", "w")
        for tp in res.keys():
            print(tp + "=============================================", file=output1)
            for rowNum in res[tp].keys():
                print(rowNum, res[tp][rowNum], file=output1)
        output1.close()

        output2 = open("classify_res_with_sentence", "w")
        for tp in res.keys():
            print(tp + "=============================================", file=output2)
            for rowNum in res[tp].keys():
                print(rowNum, res[tp][rowNum], file=output2)
                print(feedback[rowNum], file=output2)
        output2.close()




if __name__ == "__main__":
    # print(find_lcsubstr("你好123","你啊123").__len__())
    base_path = "/home/jun/Desktop/contest/sentimentAnalysis/"
    cartype = {}
    emission_mat = pickle.load(open("emission.mat", "rb"))
    user_dict = open('user.dict', 'r')
    for line in user_dict:
        sentence = list(line.strip().split(" "))[0].strip().replace(".", "").replace("-","").lower()
        cartype[sentence] = True
    user_dict.close()
    for car in extraCars:
        cartype[car] = True
    print(cartype.keys())
    print(cartype.keys().__len__())
    csvfile = open('Test.csv', 'r')
    info = []
    correct = 0
    i = 0
    carleft1 = []
    sentenceDict = {}
    jieba.load_userdict("user.dict")
    years = np.arange(1000,2020,1)
    uselessWordsDict = {}
    validflag = ["n", "eng", "m", "nrt", "ns","nrfg", "nt", "x","nz", "nr", "v", "z", "j"]
    validflagDict = {}
    for flag in validflag:
        validflagDict[flag] = True

    uselessWords = np.concatenate((years, uselessWords))
    for word in uselessWords:
        uselessWordsDict[word] = True
    feedback = {}
    for line in csvfile:
        i += 1
        sentence = list(line.strip().split('\t'))[1].strip().replace(" ","^").replace(".","你好").replace("--","你好").replace("DSG", "你好")\
            .replace("dsg", "你好").replace("tsi", "你好").replace("TSI", "你好").replace("esp", "你好")\
        .replace("ESP", "你好")
        rowNum = list(line.strip().split('\t'))[0].strip()
        feedback[rowNum] = sentence
        string = sentence.strip()
        seg = jieba.posseg.cut(string)
        prevword = ""
        sentenceDict[rowNum] = {}
        justNum = False
        justAlpha = False
        prevDash = False

        for word in seg:
            print("prevword", prevword)
            print(word.word.lower(), word.flag)
            if uselessWordsDict.__contains__(word.word.lower()) or (not validflagDict.__contains__(word.flag) and word.word.lower() != "明锐"):
                prevword, sentenceDict = output(prevword,False, word, sentenceDict, rowNum, cartype)
                continue
            prevword1 = prevword.replace("-","").lower()
            if word.word.lower() == "^":
                if (prevword1 != ""):
                    prevword = prevword + word.word
                continue
            if word.word.lower() == "-":
                if (prevword1 != ""):
                    prevword = prevword + word.word
                    prevDash = True
                continue

            isCar = False
            isAddPrev = False
            if prevDash:
                isCar = True
                isAddPrev = True
            elif cartype.__contains__(word.word.lower()):
                # print("contain")
                isCar = True
                if prevword != "":
                    for key in cartype.keys():
                        if find_lcsubstr(key, (
                            prevword1 + word.word.lower() \
                            ).replace("-", "").lower()).__len__() >= (float)(3.0/4.0 * (prevword1.__len__() + word.word.__len__())):
                            # print(key)
                            isAddPrev = True
                            break

            else:
                # if word.word.lower().__len__() <= 1:
                #     prevword, sentenceDict = output(prevword, False, word, sentenceDict, rowNum, cartype)
                #     continue
                for key in cartype.keys():
                        if word.flag == "eng" and (prevword1 == "" or onlyAlpha(prevword1)):
                            if find_lcsubstr(key, word.word.lower()) == word.word.lower():
                                isCar = True
                                if prevword1 != "" and find_lcsubstr(key, (
                                            prevword1 + word.word.lower()\
                                        ).replace("-","").lower()).__len__() == (float)(prevword1.__len__() + word.word.__len__()):
                                    isAddPrev = True
                                    break

                        elif(word.flag == "m" and (prevword1 == "" or onlyDig(prevword1))):
                            # print("hello")
                            if find_lcsubstr(key, word.word.lower()) == word.word.lower():
                                isCar = True
                                if prevword1 != "" and find_lcsubstr(key, (
                                    prevword1 + word.word.lower()).replace("-","").lower()).__len__() == \
                                        (float)(prevword1.__len__() + word.word.__len__()):
                                    isAddPrev = True
                                    break

                        elif (word.flag == "m" or "x" or "eng") and find_lcsubstr(key, word.word.lower()) == word.word.lower():
                            isCar = True
                            # print("hello")
                            if (prevword1 != "" and find_lcsubstr(key, (prevword1 + word.word.lower()).replace("-",
                                 "").lower()).__len__() >= (float)(3.0 / 4.0 *(prevword1.__len__() + word.word.__len__()))):
                                isAddPrev = True
                                break

                        else:
                            if find_lcsubstr(key, word.word.lower()).__len__() >= (float)(2.0 /3.0 *(word.word.__len__())):
                                # print("fjksajfkla")
                                isCar = True
                                if (prevword1 != "" and find_lcsubstr(key, (prevword1 + word.word.lower()).replace("-",
                                    "").lower()).__len__() > word.word.__len__()):
                                    isAddPrev = True
                                    break


            if isCar and isAddPrev:
                prevword = prevword + word.word
                prevDash = False
            else:
                # print("hello")
                #("prevword",prevword)
                prevword, sentenceDict = output(prevword, isCar, word, sentenceDict, rowNum, cartype)
        prevword, sentenceDict = output(prevword, isCar, word, sentenceDict, rowNum, cartype)

    res = {}
    res["DA"] = {}
    res["EDA"] = {}
    res["OL6"] = {}
    res["Others"] = {}
    res["Emp"] = {}
    res["ONE"] = {}



    for rowNum in sentenceDict.keys():
        # #(i, sentenceDict[i], file=testRes)
        if sentenceDict[rowNum].keys().__len__() != 0:
            put = False
            for val in sentenceDict[rowNum].keys():
                if val.__len__() == 1:
                    res["ONE"][rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif onlyDigAlpha(val):
                    res["DA"][rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif endWithDigAlpha(val):
                    res["EDA"][rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                elif val.__len__() >= 6:
                    res["OL6"][rowNum] = list(sentenceDict[rowNum].keys())
                    put = True
                    break
                else:
                    continue

            if not put:
                res["Others"][rowNum] = list(sentenceDict[rowNum].keys())
        else:
            res["Emp"][rowNum] = []

        output = open('test11-20.txt', 'w')
        for rowNum in sentenceDict.keys():
            for word in sentenceDict[rowNum].keys():
                print(rowNum, "\t", word, file=output)
        output.close()

        classify_output(res, feedback)





