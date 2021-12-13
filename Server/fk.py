#!/usr/bin/python
"""
this program responsible image split, merge, or the basic 
image matching
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
import sys
import time

app = QApplication(sys.argv)


def grab( ):
    pix = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
    return pix.toImage()

def resize(image, width, height):
    return image.scaled(width, height)

def crop(image, x, y, width, height):
    return image.copy(x, y, width, height)

def toGray(image):
    w, h = (image.width(), image.height())
    for x in range(w):
        for y in range(h):
            pixel = image.pixel(x, y)
            gray  = qGray(pixel)
            alpha = qAlpha(pixel)
            image.setPixel(x, y, qRgba(gray, gray, gray, alpha))
    return image

def getPixel(image):
    w, h = (image.width( ), image.height( ))
    pixels = [image.pixel(x, y) for x, y in zip(range(w), range(h))]
    return pixels

def getGrayPixel(image):
    w, h = (image.width( ), image.height( ))
    pixels = [qGray(image.pixel(x, y)) for x, y in zip(range(w), range(h))] 
    return pixels

def isDiff(image1, image2, gray=False):
    """
    get the two images of pixels data or gray pixels data
    and then to  judged the image1 and image2 of pixels data 
    is same or different
    """
    if gray:
        pixels1 = getGrayPixel(image1)
        pixels2 = getGrayPixel(image2)
    else:
        pixels1 = getPixel(image1)
        pixels2 = getPixel(image2)
    return sum(pixels1) != sum(pixels2)

def calculate(image1, image2):
    """
    calculate two images whether are different and find out
    which parts are different in the images  
    """  
    w, h = 1024, 768
    partWidth, partHeight = (int(w/16), int(h/16))
    pixelmap = [ ]
    for x in range(0, w, partWidth):
        for y in range(0, h, partHeight):
            chunk1 = crop(image1, x, y, partWidth, partHeight)
            chunk2 = crop(image2, x, y, partWidth, partHeight)
            if isDiff(image1=chunk1, image2=chunk2, gray=True):
                pixelmap.append([chunk2, x, y, partWidth, partHeight])
    return pixelmap

_array     = QByteArray( )
_buffer    = QBuffer(_array)
_buffer.open(QIODevice.WriteOnly)
pix = grab()
p = QPixmap.fromImage(pix)
p.save(_buffer, 'jpg')
somedata = _buffer.data()
_array.clear()
_buffer.close()
print(len(somedata))
time.sleep(4)
pix2 = grab()
updatedlist = calculate(pix, pix2)
pm = QPixmap(1920, 1080)
painter = QPainter(pm)
painter.begin(pm)
totallen = 0

for i in updatedlist:
    p = QPixmap.fromImage(i[0])
    p.save(_buffer, 'jpeg')
    # print(i)
    # print(len(_buffer.data()))
    totallen += len(somedata)
    painter.drawImage(i[1], i[2], i[0])
painter.end()
pm.save(_buffer, 'jpeg')
somedata = _buffer.data()
# print(len(somedata))
print(totallen)
window = QMainWindow()
widget = QWidget()
vbox = QVBoxLayout()
label = QLabel()
pixmap = QPixmap.fromImage(pix)
label.setPixmap(pm)
vbox.addWidget(label)
widget.setLayout(vbox)
window.setCentralWidget(widget)
window.show()
sys.exit(app.exec())