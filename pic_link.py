from __future__ import division
from PIL import Image

import numpy
import numexpr
import os
import os.path
import random

path = r'/home/xcv/learning_python/scrapy/picture'
bigPhoto = r'/home/xcv/learning_python/scrapy/big.jpg'

aval = []

W_num = 25
H_num = 25
W_size = 360
H_size = 640
alpha = 0.3

#获得所有照片信息
def getAllPhotos():
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            endName = os.path.splitext(filename)[-1]
            if endName == '.jpg' or endName == '.png':
                aval.append(os.path.join(parent, filename))

#将照片转为一样的大小
def transfer(img_path, dst_width, dst_height):
    im = Image.open(img_path)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    s_w, s_h = im.size
    if s_w > s_h:
        im = im.rotate(90)

    resized_img = im.resize((dst_width, dst_height), Image.ANTIALIAS)
    resized_img = resized_img.crop((0, 0, dst_width, dst_height))
    return resized_img

#照片拼接
def link_pics():
    iW_size = W_num * W_size
    iH_size = H_num * H_size
    I = numpy.array(transfer(bigPhoto, iW_size, iH_size))
    #I = numexpr.evaluate("""I*(1-alpha)""")
    for i in range(W_num):
        for j in range(H_num):
             temp = I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)]
             res = numexpr.evaluate("""temp*(1-alpha)""")
             I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)] = res

    for i in range(W_num):
        for j in range(H_num):
            SH = I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)]
            DA = transfer(random.choice(aval), W_size, H_size)
            res  = numexpr.evaluate("""SH+DA*alpha""")
            I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)] = res
    img = Image.fromarray(I.astype(numpy.uint8))
    img = img.point(lambda i : i * 1.5)
    img.save('new_image.jpg')

#第二种算法,这里会发生内存溢出的错误，可能运算量太大
def link_pics2():
    iW_size = W_num * W_size
    iH_size = H_num * H_size
    I = numpy.array(transfer(bigPhoto, iW_size, iH_size)) * 1.0

    for i in range(W_num):
        for j in range(H_num):
            s = random.choice(aval)
            res = I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] * numpy.array(transfer(s, W_size, H_size))/255
            I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] = res

    img = Image.fromarray(I.astype(numpy.uint8))
    img = img.point(lambda i : i * 1.5)
    img.save("createNevImg_past.jpg")

if __name__ == '__main__':
    getAllPhotos()
    link_pics()



