# usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import sys
import csv
import pandas as pd
import numpy as np
import datetime
import time
import random
import requests
import os
import codecs
import mmap
import contextlib
from django.conf import settings

class sensitiveClass:
    def __init__(self):
        self = self

    def bubble_sort(self,nums):
        repeatedText = []
        for i in range(len(nums)):  
            for j in range(len(nums)): 
                if i!=j and nums[i] in nums[j]:
                    repeatedText.append(nums[i])
        repeatedText = list(set(repeatedText)) 
        for text in  repeatedText:
            if text in nums:
                nums.remove(text)  
        return nums
    def bubble_sort_1(self,nums):
        repeatedText = []
        for i in range(len(nums)):  
            for j in range(len(nums)): 
                if i!=j and nums[i] in nums[j]:
                    repeatedText.append(nums[i])
        repeatedText = list(set(repeatedText)) 
        return repeatedText

    def check_sensitiveWords_test(self, df, input_word):
        t = time.time()
        startTime = int(round(t * 1000))
        temp_flag = 0 #敏感词临时标记
        sensitive_hit_flag = 0 #0-五敏感词  1-有敏感词
        sensitive_list = [] #敏感词列表
        sensitive_size = 0    #敏感词数量
        list_index = 0
        web_text = "<div>"
        app_text = ""
        original_text = input_word
        final_text = ""
        keyword_arr = []

        totalLength = 0
        for index, row in df.iterrows():
            sensitiveCms = row['内容'].split('、')
            totalLength = totalLength + len(sensitiveCms)
            for keyword in sensitiveCms:
                if keyword.strip()=='':
                    break
                if keyword in input_word:
                    result = {}
                    result["firstType"] = row['大类']
                    result["secondType"] = row['次类']
                    result["keyword"] = keyword
                    temp_flag = 1
                    sensitive_hit_flag = 1
                    sensitive_size = sensitive_size + 1
                    sensitive_list.append(result)
                if (temp_flag == 1):
                    keyword_arr.append(keyword)
                    temp_flag = 0
                else:
                    temp_flag = 0
            

        t = time.time()
        endTime = int(round(t * 1000))
        resultMap = {} 
        
        sensitive_list_result = []
        temp_map = {}
        #tmp_map = {}
        aList = []
        for each in sensitive_list:
            temp_map = each
            aList.append(temp_map["firstType"])
        aList = list(set(aList)) 
        keyword_arr_sort = list(set(keyword_arr))

        removeRepeartedArra = sensitiveClass().bubble_sort(keyword_arr_sort)

        removeRepeartedArra1 = sensitiveClass().bubble_sort_1(keyword_arr)
        web_text = input_word
        app_text = input_word
        for text in removeRepeartedArra:
            web_text = web_text.replace(text, "<span style='color:red'>"+text+"</span>")
            app_text = app_text.replace(text, "<font color ='red' size='20'>"+text+"</font>")
        for text in removeRepeartedArra1:
            web_text = web_text.replace(text, "<span style='color:red'>"+text+"</span>")
            app_text = app_text.replace(text, "<font color ='red' size='20'>"+text+"</font>")    

        t = time.time()
        endTime = int(round(t * 1000))
        resultMap["sensitive_hit_flag"] = sensitive_hit_flag
        resultMap["sensitive_size"] = sensitive_size
        resultMap["sensitive_list"] = sensitive_list
        resultMap["final_list"] = aList
        resultMap["web_text"] = "<div>"+web_text+"</div>"
        resultMap["app_text"] = app_text
        
        return resultMap

    def check_sensitiveWords(self, input_word):
        t = time.time()
        startTime = int(round(t * 1000))
        temp_flag = 0 #敏感词临时标记
        sensitive_hit_flag = 0 #0-五敏感词  1-有敏感词
        sensitive_list = [] #敏感词列表
        sensitive_size = 0    #敏感词数量
        list_index = 0
        web_text = ""
        app_text = ""
        original_text = input_word
        final_text = ""
        keyword_arr = []

        totalLength = 0
        for index, row in settings.DF.iterrows():
            sensitiveCms = row['内容'].split('、')
            totalLength = totalLength + len(sensitiveCms)
            for keyword in sensitiveCms:
                if keyword.strip()=='':
                    break
                if keyword in input_word:
                    result = {}
                    result["firstType"] = row['大类']
                    result["secondType"] = row['次类']
                    result["keyword"] = keyword
                    temp_flag = 1
                    sensitive_hit_flag = 1                    
                    sensitive_list.append(result)
                if (temp_flag == 1):
                    keyword_arr.append(keyword)
                    temp_flag = 0
                else:
                    temp_flag = 0

        t = time.time()
        endTime = int(round(t * 1000))
        resultMap = {}         
        sensitive_list_result = []
        temp_map = {}
        #tmp_map = {}
        aList = []
        for each in sensitive_list:
            temp_map = each
            aList.append(temp_map["firstType"])
        aList = list(set(aList)) 
        keyword_arr_sort = list(set(keyword_arr))
        removeRepeartedArra = sensitiveClass().bubble_sort(keyword_arr_sort)
        removeRepeartedArra1 = sensitiveClass().bubble_sort_1(keyword_arr)
        web_text = input_word
        app_text = input_word
        sensitive_list_result = []
        for text in removeRepeartedArra:
            web_text = web_text.replace(text, "<span style='color:red'>"+text+"</span>")
            app_text = app_text.replace(text, "<font color ='red' size='20'>"+text+"</font>")
            for s in sensitive_list:
                kw = s["keyword"]
                if kw == text:                    
                    sensitive_list_result.append(s)
        for text in removeRepeartedArra1:
            web_text = web_text.replace(text, "<span style='color:red'>"+text+"</span>")
            app_text = app_text.replace(text, "<font color ='red' size='20'>"+text+"</font>")                    
        t = time.time()
        endTime = int(round(t * 1000))        
        resultMap["sensitive_list"] = sensitive_list
        resultMap["final_list"] = aList
        
        resultMap["sensitive_hit_flag"] = sensitive_hit_flag
        resultMap["sensitive_size"] = sensitive_size
        resultMap["web_text"] = "<div>"+web_text+"</div>"
        resultMap["app_text"] = app_text
        resultMap["takingTimes"] = endTime - startTime
        return resultMap

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(),"backend","api","sensitives","sensitiveWords.csv"),encoding='gbk')
    #sensitiveClass().check_sensitiveWords_test(df, "十八摸 11111")
    sensitiveClass().check_sensitiveWords_test(df, " 十八摸  我是台独分子   台独分子  独分子 台独 十八摸 台独共党")
    #sensitiveClass().check_sensitiveWords_test(df, "  heheh ")
    #sensitiveClass().check_sensitiveWords_test(df, "你 不是 跟 我 讲的 笑话 吗 欲死欲仙 十八摸")
    
