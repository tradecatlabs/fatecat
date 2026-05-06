#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
import random

def getLeft(n):
    random.seed("asdfasdf")
    return np.random.randint(5, n-4+1)

def getYao():
    n = 49
    for i in range(3):
        leftSplit = getLeft(n)
        rightSplit = n-leftSplit
        left = leftSplit-1
        right = rightSplit
        reduceFromLeft = left % 4
        if reduceFromLeft == 0:
            reduceFromLeft += 4
        left=left-reduceFromLeft
        reduceFromRight = right % 4
        if reduceFromRight == 0:
            reduceFromRight += 4
        right=right-reduceFromRight
        n=left+right
    yao = left/4+right/4
    return yao

def getGua():
    yao=[]
    for j in range(6):
        yao.append(getYao())
    yao.reverse()
    return yao

def getZhiGua(gua):
    zhigua=[]
    for i in range(6):
        if gua[i]==9:
            zhigua.append(8)
        elif gua[i]==6:
            zhigua.append(7)
        else:
            zhigua.append(gua[i])
    return zhigua

def getPartGua(gua):
    for i in range (3):
        gua[i]=gua[i]%2
    result = gua[0]+gua[1]*2+gua[2]*4
    returnValue=['坤','艮','坎','巽','震','离','兑','乾']
    return returnValue[result]

def guaNum(gua):
    returnValue=['坤','艮','坎','巽','震','离','兑','乾']
    return returnValue.index(gua)

def getGuaName(shang, xia):
    order = str(guaNum(shang))+str(guaNum(xia))
    guaDict = '77乾$73姤$71遁$70否$30观$10剥$50晋$57大有$66兑$62困$60萃$61咸$21蹇$01谦$41小过$46归妹$55离$51旅$53鼎$52未济$12蒙$32涣$72讼$75同人$44震$40豫$42解$43恒$03升$23井$63大过$64随$33巽$37小畜$35家人$34益$74无妄$54噬嗑$14颐$13蛊$22坎$26节$24屯$25既济$65革$45丰$05明夷$02师$11艮$15贲$17大畜$16损$56睽$76履$36中孚$31渐$00坤$04复$06临$07泰$47大壮$67夬$27需$20比$'
    pos = guaDict.find(order)
    returnStr = ''
    i=0
    while guaDict[pos+i]<>'$':
        i+=1
    returnStr = guaDict[pos+2:pos+i]
    return returnStr

def getGuaCi(gua):
    for line in open('guaci','r'):
        guaci=line.strip('\n')
        if guaci[:guaci.find('，')]==gua:
            return guaci

def printInfo(gua, zhiGua, printChar):
    yangYao=printChar+printChar+printChar
    yinYao=yangYao+'   '+yangYao
    yangYao=yangYao+yangYao+yangYao
    guaShang = getPartGua(gua[0:3])
    guaXia = getPartGua(gua[3:])
    zhiGuaShang = getPartGua(zhiGua[0:3])
    zhiGuaXia = getPartGua(zhiGua[3:])
    yuanGuaName =  getGuaName(guaShang, guaXia)
    zhiGuaName = getGuaName(zhiGuaShang, zhiGuaXia)
    print '     原卦:'+yuanGuaName+'\t              之卦:'+zhiGuaName
    for i in range(6):
        toPrintChange='   '
        if gua[i]==7 or gua[i]==9:
            toPrintGua = yangYao
        else:
            toPrintGua = yinYao
        if zhiGua[i]==7 or zhiGua[i]==9:
            toPrintZhiGua = yangYao
        else:
            toPrintZhiGua = yinYao
        if zhiGua[i]<>gua[i]:
            toPrintChange='  *'
        if i==1:
            print (str(gua[i])+':  '+toPrintGua+toPrintChange+' '+guaShang+'      '+str(zhiGua[i])+':  '+toPrintZhiGua)+'    '+zhiGuaShang
        elif i==4:
            print (str(gua[i])+':  '+toPrintGua+toPrintChange+' '+guaXia+'      '+str(zhiGua[i])+':  '+toPrintZhiGua)+'    '+zhiGuaXia
        else:
            print (str(gua[i])+':  '+toPrintGua+toPrintChange+'         '+str(zhiGua[i])+':  '+toPrintZhiGua)
    print ('\n')
    print getGuaCi(yuanGuaName)
    print getGuaCi(zhiGuaName)
    print ('\n\n\n\n\n')


# Main
gua = getGua()
zhiGua = getZhiGua(gua)
printInfo(gua, zhiGua, '=')