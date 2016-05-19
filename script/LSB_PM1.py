#coding:utf-8

__author__ = 'g9752'

import PIL
import Image
import struct
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wx.lib.pubsub import pub as Publisher
import random

def bit2list(byte):
    """
    将一个byte值转换成长度为8的字符列表，列表元素类型为 char
    :param byte: byte值
    :return: 长度为8的列表
    """

    byte = struct.unpack("B",byte)
    byte_b = bin(byte[0])          # 转成二进制
    byte_l = list(byte_b)       # 转成列表
    byte_l = byte_l[2:]         # 列表切片修饰
    while len(byte_l) < 8:      # 列表填充
        byte_l.insert(0,'0')
    return byte_l

def dstfile2list(filename):
    """
    将文件转换成0,1的字节串的列表
    :param filename: 源文件名
    :return: 由文件二进制值组成的列表
    """
    fp = open(filename,'rb')
    bitlist = []
    byte = fp.read(1)
    while byte != "":
        bitlist += bit2list(byte)
        byte = fp.read(1)
    fp.close()
    return bitlist

def AppendEndFlag(bitlist,flag="LSB"):
    """
    向bitlist中追加结束标志
    :param bitlist: 原bit列表
    :param flag: 默认结束标志 "LSB"
    :return: 添加结束标志后的 bit列表
    """
    for i in range(len(flag)):
        #byte = struct.unpack("b",flag[i])
        bitlist += bit2list(flag[i])
    return bitlist

def LSB(src,dst,tofile,flag):
    """
    实现LSB-PM1的功能代码
    :param src: 源图片文件路径
    :param dst: 隐写文件路径
    :param tofile: 输出文件路径
    :param flag: 标志参数，用于控制隐写时使用的位置
    :return: 一个元组，1：结果   2：提示信息
    """
    bitlist = dstfile2list(dst)         #将目标文件转换成比特列表
    bitlist = AppendEndFlag(bitlist)    #向比特列表中追加结束标志

    ibitlist = 0
    try:
        im = Image.open(src)
        rgb_im = im.convert("RGB")
        width,height = im.size
        for i in range(0,width):
            for j in range(0,height):
                r,g,b = rgb_im.getpixel((i,j))
                r1,g1,b1 = r,g,b
                # R
                if ibitlist < len(bitlist):
                    ele = bitlist[ibitlist]
                    if ele == '0' and r % 2 == 1:
                        r1 = r + random.choice((-1,1))
                    if ele == '1' and r % 2 == 0:
                        r1 = r + random.choice((-1,1))
                    if r1 > 254:
                        r1 = r1 - 2
                    if r1 < 0 :
                        r1 = r1 + 2
                    ibitlist += 1
                # G
                if ibitlist < len(bitlist):
                    ele = bitlist[ibitlist]
                    if ele == '0' and g % 2 == 1:
                        g1 = g + random.choice((-1,1))
                    if ele == '1' and g % 2 == 0:
                        g1 = g + random.choice((-1,1))
                    if g1 > 254:
                        g1 = g1 - 2
                    if g1 < 0:
                        g1 = g1 + 2
                    ibitlist += 1
                # B
                if ibitlist < len(bitlist):
                    ele = bitlist[ibitlist]
                    if ele == '0' and b % 2 == 1:
                        b1 = b + random.choice((-1,1))
                    if ele == '1' and b % 2 == 0:
                        b1 = b + random.choice((-1,1))
                    if b1 > 254:
                        b1 = b1 - 2
                    if b1 < 0:
                        b1 = b1 + 2
                    ibitlist += 1

                rgb_im.putpixel((i,j),(r1,g1,b1))
                #print (i,j),(r,g,b),(r1,g1,b1)
        rgb_im.save(tofile)
        pass

    finally:
        pass
    return (True,u"成功完成LSB算法")

def list2byte(lb):
    """
    将长度为8的bit列表转换成一个byte
    :param lb: 长度为8的bit列表
    :return: 根据列表转成的byte
    """
    try:
        byte = 0
        for i in range(len(lb)):
            if lb[i] == 1:
                byte = byte << 1
                byte = byte | 1
            if lb[i] == 0:
                byte = byte << 1
        #print byte
        byte = struct.pack('B',byte)
        #print byte
        return byte
    except Exception:
        print lb


def deLSB(src,tofile):
    """
    该方法完成LSB-PM1的解密功能
    :param src: 包含隐写信息的图片文件
    :param tofile: 解密出的隐写文件的保存路径
    :return: 结果元组 1:执行结果 2:提示信息
    """
    tofile = open(tofile,"wb")
    bytelist = []
    im = Image.open(src)
    rgb_im = im.convert("RGB")
    width,height = rgb_im.size
    for i in range(width):
        for j in range(height):
            r,g,b = rgb_im.getpixel((i,j))

            #r
            if r % 2 == 0:  #R的最低位为0
                bytelist.append(0)
            if r % 2 == 1:  #R的最低位为1
                bytelist.append(1)

            #g
            if g % 2 == 0:  #G的最低位为0
                bytelist.append(0)
            if g % 2 == 1:  #G的最低位为1
                bytelist.append(1)

            #r
            if b % 2 == 0:  #B的最低位为0
                bytelist.append(0)
            if b % 2 == 1:  #B的最低位为1
                bytelist.append(1)
    print len(bytelist)
    """
    获取flag的bit列表
    """
    flag = "LSB"
    flag_l = []
    for i in range(len(flag)):
        flag_l += bit2list(flag[i])
    flag_l = map(int,flag_l)

    while len(bytelist) != 0:
        tmp = []
        for t in range(8):
            tmp.append(bytelist.pop(0))

        byte = list2byte(tmp)
        if byte == "L":
            for j in range(8,len(flag_l)):
                if flag_l[j] != bytelist[j-8]:
                    break
            else:
                tofile.close()
                return (True,u"成功从图片中提取到隐写信息")

        tofile.write(byte)
        tofile.flush()
    tofile.close()
    return (True,u"成功从图片中提取到隐写信息")
    pass

if __name__ == "__main__":
    LSB(u"./example/hei.bmp",u"./example/1.zip",u"./example/out.bmp","")
    deLSB(u"./example/out.bmp",u"./example/out.zip")
    #print list2byte([0,1,0,1,0,0,0,0])
    print "OK"
    pass