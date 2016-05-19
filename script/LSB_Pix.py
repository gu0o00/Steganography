#coding:utf-8
__author__ = 'g9752'

from PIL import Image

masklist = [0b11111110,
            0b11111100,
            0b11111000,
            0b11110000,
            0b11100000,
            0b11000000,
            0b10000000]

def LSB_Pix(src,dst,tofile,level):
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

    #统一原图与隐写图的图像大小
    dst_im = dst_im.resize(src_im.size,Image.ANTIALIAS)

    #保存 测试
    #src_im.save(".\example\src.png")
    #dst_im.save(".\example\dst.png")
    pattern = masklist[level]
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
    dst_im.save(tofile)
    pass

def deLSB_Pix(src,tofile,level):
    """
    实现LSB_Pix的解密过程
    :param src:包含隐写信息图片的路径
    :param tofile:生成文件保存路径
    :param level:提取的像素等级
    :return:结果元组
    """
    im = Image.open(src).convert("RGB")
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r,g,b = im.getpixel((i,j))

            r = r & ~masklist[level]
            r = r << (8-level)

            g = g & ~masklist[level]
            g = g << (8-level)

            b = b & ~masklist[level]
            b = b << (8-level)

            im.putpixel((i,j),(r,g,b))

    im.save(tofile)
    pass

if __name__ == "__main__":
    #LSB_Pix("C:\Users\g9752\PycharmProjects\Steganography\example\longmao1.bmp",r"C:\Users\g9752\PycharmProjects\Steganography\example\xingkong.png","C:\Users\g9752\PycharmProjects\Steganography\example\dst3.bmp",4)

    deLSB_Pix("C:\Users\g9752\PycharmProjects\Steganography\example\dst3.bmp",4)
    pass