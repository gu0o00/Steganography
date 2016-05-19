#coding:utf-8

__author__ = 'g9752'

#import wx
#import PIL
#import Image
#import numpy as np
#import matplotlib.pyplot as plt
import struct
from PIL import Image
from wx.lib.pubsub import pub as Publisher
import threading
import time

masklist = [0b11111110,
            0b11111100,
            0b11111000,
            0b11110000,
            0b11100000,
            0b11000000,
            0b10000000]

class LSB_Pix_Thread(threading.Thread):
    def __init__(self,src,dst,tofile,level):
        threading.Thread.__init__(self)
        self.src = src
        self.dst = dst
        self.tofile = tofile
        self.level = level
        pass

    def run(self):
        starttime = time.clock()
        self.Encrypt(self.src,self.dst,self.tofile,self.level)
        endtime = time.clock()
        print "encrypt use time:", endtime-starttime
        pass

    def Encrypt(self,src,dst,tofile,level):
        """
        实现LSB_Pix 算法
        :param src:源图片文件路径
        :param dst:欲隐藏图片文件的路径
        :param tofile:生成文件保存路径
        :param level:隐藏像素的等级
        :return:结果元组
        """
        src_im = Image.open(src).convert("RGB")
        dst_im = Image.open(dst).convert("RGB")
        level = level - 1
        #统一原图与隐写图的图像大小
        dst_im = dst_im.resize(src_im.size,Image.ANTIALIAS)

        #保存 测试
        #src_im.save(".\example\src.png")
        #dst_im.save(".\example\dst.png")
        pattern = masklist[level]
        width,height = src_im.size
        for i in range(src_im.size[0]):
            for j in range(src_im.size[1]):
                ori_r,ori_g,ori_b = src_im.getpixel((i,j))
                dst_r,dst_g,dst_b = dst_im.getpixel((i,j))

                ori_r = ori_r & pattern
                dst_r = dst_r >> level
                r1 = ori_r | dst_r

                ori_g = ori_g & pattern
                dst_g = dst_g >> level
                g1 = ori_g | dst_g

                ori_b = ori_b & pattern
                dst_b = dst_b >> level
                b1 = ori_b | dst_b

                dst_im.putpixel((i,j),(r1,g1,b1))
                """
                回送进度消息
                """
                process = (i) * height + j
                process = float(process) * 100 / (width * height)
                Publisher.sendMessage("updateGauge_pix",message=process)
        dst_im.save(tofile)
        Publisher.sendMessage("updateGauge_pix",message=100)
        print "save file"

        return (True,u"成功完成LSB算法")

class DeLSB_Thread(threading.Thread):
    def __init__(self,src,tofile,level):
        threading.Thread.__init__(self)
        self.src = src
        self.tofile = tofile
        self.level = level

    def run(self):
        starttime = time.clock()
        self.Decrypt(self.src,self.tofile,self.level)
        endtime = time.clock()
        print "decrypt use time:", endtime-starttime
        pass

    def Decrypt(self,src,tofile,level):
        """
        实现LSB_Pix的解密过程
        :param src:包含隐写信息图片的路径
        :param tofile:生成文件保存路径
        :param level:提取的像素等级
        :return:结果元组
        """
        im = Image.open(src).convert("RGB")
        level = level - 1
        width,height = im.size
        for i in range(width):
            for j in range(height):
                r,g,b = im.getpixel((i,j))
                """
                添加解密过程：从像素信息中提取隐写数据加入到bypelist中
                """
                r,g,b = im.getpixel((i,j))

                r = r & ~masklist[level]
                r = r << (8-level)

                g = g & ~masklist[level]
                g = g << (8-level)

                b = b & ~masklist[level]
                b = b << (8-level)

                im.putpixel((i,j),(r,g,b))

                """
                回送进度消息
                """
                process = (i) * height + j
                process = process * 100 / (width * height)
                Publisher.sendMessage("updateGauge_pix",message=process)
        im.save(tofile)
        Publisher.sendMessage("updateGauge_pix",message=100)
        return (True,u"成功从图片中提取到隐写信息")
        pass

if __name__ == "__main__":
    pass