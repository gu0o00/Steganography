#coding:utf-8

__author__ = 'g9752'
import os


def TailAppend(src,dst,tofile):
    """
    实现尾部追加功能的具体代码
    :param src: 源图片路径
    :param dst: 隐写文件路径
    :param tofile:结果文件的保存路径
    :return:返回一个元组，第一个值显示结果，第二个值显示提示
    """
    if os.path.isfile(src) == False:
        return (False,u"图片文件不存在")
    if os.path.isfile(dst) == False:
        return (False,u"隐写文件不存在")

    afile = open(src,'rb')
    bfile = open(dst,'rb')
    tofile = open(tofile,'wb')
    try:
        byte = afile.read(1)
        while byte != '':
            tofile.write(byte)
            byte = afile.read(1)

        byte = bfile.read(1)
        while byte != '':
            tofile.write(byte)
            byte = bfile.read(1)
    finally:
        afile.close()
        bfile.close()
        tofile.close()
    return (True,u"文件合并成功")

if __name__ == "__main__":
    TailAppend(u"./example/longmao1.jpg",u"./example/1.zip",u"./example/out.jpg")