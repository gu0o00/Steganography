#coding:utf-8

__author__ = 'g9752'

import wx
import PIL
import Image
import struct
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wx.lib.pubsub import pub as Publisher
import threading

class Encrypt_Thread(threading.Thread):
    def __init__(self,src,dst,tofile):
        threading.Thread.__init__(self)
        self.src = src
        self.dst = dst
        self.tofile = tofile
        pass

    def run(self):
        self.Encrypt(self.src,self.dst,self.tofile)
        pass

    def bit2list(self,byte):
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

    def dstfile2list(self,filename):
        """
        将文件转换成0,1的字节串的列表
        :param filename: 源文件名
        :return: 由文件二进制值组成的列表
        """
        fp = open(filename,'rb')
        bitlist = []
        byte = fp.read(1)
        while byte != "":
            bitlist += self.bit2list(byte)
            byte = fp.read(1)
        fp.close()
        return bitlist

    def AppendEndFlag(self,bitlist,flag="LSB"):
        """
        向bitlist中追加结束标志
        :param bitlist: 原bit列表
        :param flag: 默认结束标志 "LSB"
        :return: 添加结束标志后的 bit列表
        """
        for i in range(len(flag)):
            #byte = struct.unpack("b",flag[i])
            bitlist += self.bit2list(flag[i])
        return bitlist


    def Encrypt(self,src,dst,tofile,flag=None):
        """
        注释
        :param src:
        :param dst:
        :param tofile:
        :param flag:
        :return:
        """

        bitlist = self.dstfile2list(dst)
        bitlist = self.AppendEndFlag(bitlist)    #向字节列表中追加结束标志

        ibitlist = 0
        try:
            im = Image.open(src)
            rgb_im = im.convert("RGB")
            width,height = im.size
            total = width * height
            for i in range(0,width):
                for j in range(0,height):
                    r,g,b = rgb_im.getpixel((i,j))
                    r1,g1,b1 = r,g,b
                    """
                    添加加密过程
                    """

                    rgb_im.putpixel((i,j),(r1,g1,b1))
                    #print (i,j),(r,g,b),(r1,g1,b1)
                    """
                    回送进度消息
                    """
                    process = (i) * height + j
                    process = process * 100 / total
                    Publisher.sendMessage("updateGauge",message=process)

            rgb_im.save(tofile)
            Publisher.sendMessage("updateGauge",message=100)
            pass

        finally:
            pass
        return (True,u"成功完成LSB算法")

class DeLSB_Thread(threading.Thread):
    def __init__(self,src,tofile):
        threading.Thread.__init__(self)
        self.src = src
        self.tofile = tofile

    def run(self):
        self.Decrypt(self.src,self.tofile)

    def list2byte(self,lb):
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
            byte = struct.pack('B',byte)
            return byte
        except Exception:
            print lb

    def bit2list(self,byte):
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

    def Decrypt(self,src,tofile):
        """
        注释
        :param src:
        :param tofile:
        :return:
        """
        tofile = open(tofile,"wb")
        bytelist = []
        im = Image.open(src)
        rgb_im = im.convert("RGB")
        width,height = rgb_im.size
        for i in range(width):
            for j in range(height):
                r,g,b = rgb_im.getpixel((i,j))
                """
                添加解密过程：从像素信息中提取隐写数据加入到bypelist中
                """


                """
                回送进度消息
                """
                process = (i) * height + j
                process = process * 50 / (width * height)
                Publisher.sendMessage("updateGauge",message=process)
        print len(bytelist)
        len_list = len(bytelist)
        """
        获取flag的bit列表
        """
        flag = "LSB"
        flag_l = []
        for i in range(len(flag)):
            flag_l += self.bit2list(flag[i])
        flag_l = map(int,flag_l)

        while len(bytelist) != 0:
            tmp = []
            for t in range(8):
                tmp.append(bytelist.pop(0))

            """
            回送进度消息
            """
            process = ((len_list - len(bytelist)) * 50 / len_list) + 50
            Publisher.sendMessage("updateGauge",message=process)

            byte = self.list2byte(tmp)
            if byte == "L":
                for j in range(8,len(flag_l)):
                    if flag_l[j] != bytelist[j-8]:
                        break
                else:
                    Publisher.sendMessage("updateGauge",message=101)
                    tofile.close()
                    return (True,u"成功从图片中提取到隐写信息")

            tofile.write(byte)
            tofile.flush()
        tofile.close()
        return (True,u"成功从图片中提取到隐写信息")
        pass

if __name__ == "__main__":
    pass