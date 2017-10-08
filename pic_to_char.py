#encoding:utf-8

from __future__ import division
from PIL import Image

def conver2char(image_name):
    img = Image.open(image_name).convert('L')
    w, h = img.size
    if w > 100:
        h = int((100/w) * h / 2)
        w = 100
    #滤镜消除锯齿
    img1 = img.resize((w, h), Image.ANTIALIAS)
    char = [' ', ',', '1', '+', 'n', 'D', '@', 'M']
    f = open(image_name + '.txt', 'w')
    for j in range(h):
        line = ''
        for i in range(w):
            for k in range(0, 8):
                if img1.getpixel((i, j)) < (k + 1) *32:
                    line += char[7-k]
                    break
        f.write(line + '\n')
    f.close()

if __name__ == '__main__':
    conver2char('cat.jpg')

