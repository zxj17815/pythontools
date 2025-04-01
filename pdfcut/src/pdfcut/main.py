#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :main.py
@Description :裁剪pdf文件
@DateTiem    :2022-11-16 13:38:14
@Author      :Jay Zhang
'''


import sys
import fitz
import os
import datetime


def pdfcut(pdfPath, outPath):
    print("outPath="+outPath)
    pdfDoc = fitz.open(pdfPath)

    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        print(page)
        doc = fitz.open()
        doc.insertPDF(pdfDoc, from_page=pg, to_page=pg)
        doc.save(outPath+str(pg)+".pdf")


if __name__ == "__main__":
    pdfPath = 'pdf/test.pdf'
    outPath = 'out/'
    pdfcut(pdfPath, outPath)
