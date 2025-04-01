#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :cut_main_object.py
@Description :Image processing tools based on cv2,numpy
@DateTiem    :2020-07-01 13:10:26
@Author      :Jay Zhang
'''

import os
import numpy as np
import cv2

class CutMainObject():

    def __init__(self,image_path,out_path="",out_name="test",out_height=None,out_width=None):
        """Crop out the largest inspection-free pattern in the image
        """
        self.image_path=os.path.abspath(image_path)
        self.out_path=os.path.abspath(out_path)
        self.out_name=out_name
        self.out_height=out_height
        self.out_width=out_width
        self.img=cv2.imread(image_path)
        b_channel, g_channel, r_channel = cv2.split(self.img)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        alpha_channel[:, :int(b_channel.shape[0] / 2)] = 255
        self.img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    def _ProcessingImg(self):
        """Processing pictures The final period is a binary map (black and white)
        """
        img=self.img # 原图 
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(img,kernel,iterations=1) # 模糊
        img_gray = cv2.cvtColor(erosion,cv2.COLOR_BGR2GRAY) # 灰度图
        ret, binary = cv2.threshold(img_gray,230,255,cv2.THRESH_BINARY) # 黑白 二值图
        return binary

    def _GetMainObjectContoursRect(self,binary):
        """Get the largest object (area) in the outline
        """
        contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 获取图片所有轮廓
        contours.remove(contours[0])
        main_object=[]
        main_area=0.0
        for target in contours:
            if cv2.contourArea(target)>main_area:
                main_area=cv2.contourArea(target)
                main_object=target
        rect = cv2.minAreaRect(main_object)
        return rect,main_object

    def _CutOut(self,rect,main_object):
        box = np.int0(cv2.boxPoints(rect))
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        hight = y2 - y1
        width = x2 - x1
        mask = np.zeros_like(self.img_BGRA)
        cv2.drawContours(mask, [main_object], -1, (255,255,255,255), -1)
        mask[mask == (255,255,255,255)] = self.img_BGRA[mask == ((255,255,255,255))]
        cropImg = mask[y1:y1+hight, x1:x1+width]
        return cropImg

    def Save(self):
        rect,main_object=self._GetMainObjectContoursRect(self._ProcessingImg())
        cropImg=self._CutOut(rect,main_object)
        if self.out_height and self.out_width:
            cropImg=cv2.resize(cropImg,(self.out_height,self.out_width))
        cv2.imwrite(self.out_path+"/"+self.out_name+".png", cropImg)
        return self.out_path+"/"+self.out_name+".png"

    def _Show(self):
        """just test， show GUI
        """
        rect,main_object=self._GetMainObjectContoursRect(self._ProcessingImg())
        cropImg=self._CutOut(rect,main_object)
        while(1):
            cv2.imshow('img',self.img)
            cv2.imshow('cropImg',cropImg)
            cv2.imshow('RGBA',self.img_BGRA)
            k=cv2.waitKey(1)
            if k == ord('q'):#按q键退出
                break
        cv2.destroyAllWindows()
