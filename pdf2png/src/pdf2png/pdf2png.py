#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :pdf2png.py
@Description :用于把pdf转换为png图片的
@DateTiem    :2022-07-02 13:37:40
@Author      :Jay Zhang
'''

import datetime
import os

import fitz
from PIL import Image as PIL_Image


def combine2Pdf(folderPath, pdfFilePath):
    files = os.listdir(folderPath)
    pngFiles = []
    sources = []
    for file in files:
        if 'png' in file:
            pngFiles.append(folderPath + '/' + file)
    pngFiles.sort()
    print(pngFiles)
    output = PIL_Image.open(pngFiles[0])
    pngFiles.pop(0)
    for file in pngFiles:
        pngFile = PIL_Image.open(file)
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert("RGB")
        sources.append(pngFile)
    output.save(pdfFilePath + '/result.pdf', "pdf",
                save_all=True, append_images=sources)


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    i = 1
    count = pdfDoc.page_count
    print('count', count)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 3  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 3
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        (filepath, tempfilename) = os.path.split(pdfPath)
        (filename, extension) = os.path.splitext(tempfilename)
        if not os.path.exists(imagePath + '/' + 'images_%s' % filename):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath + '/' + 'images_%s' %
                        filename)  # 若图片文件夹不存在就创建
        print(imagePath + '/' + 'images_%s/%s.png' % (filename, i))
        pix.save(imagePath + '/' + 'images_%s/%s.png' %
                 (filename, i))  # 将图片写入指定的文件夹内
        p = imagePath + '/' + 'images_%s' % filename
        if i == count:
            combine2Pdf(p, p)
        i = i + 1

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


if __name__ == "__main__":
    pdfPath = os.listdir('pdf')
    imagePath = 'images'
    for pdf in pdfPath:
        if 'pdf' in pdf:
            pyMuPDF_fitz('pdf/' + pdf, imagePath)
