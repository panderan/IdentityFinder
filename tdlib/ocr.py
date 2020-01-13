#!/usr/bin/env python
''' OCR
'''
import os
import numpy as np
import cv2
import pytesseract
from PIL import Image
from tdlib.common import crop_rect, tdHighConstract

class TdOCR:
    ''' TdOCR
    '''
    def __init__(self):
        pass

    def ocr(self, tls, color_image, name):
        ''' ocr 识别
        Args
            tls 文本区域
            image 文本图像
        Return
            List 文本列表
        '''
        b, g, r = color_image[:, :, 0], color_image[:, :, 1], color_image[:, :, 2]
        texts = []
        for i, tl in enumerate(tls):
            topleftp = (tl[:, 0].min(), tl[:, 1].min())
            tli_r = tdHighConstract(np.uint8(self._prep(crop_rect(r, tl)[0])))
            tli_g = tdHighConstract(np.uint8(self._prep(crop_rect(g, tl)[0])))
            tli_b = tdHighConstract(np.uint8(self._prep(crop_rect(b, tl)[0])))
            tl_image = np.zeros((tli_b.shape[0], tli_b.shape[1], 3))
            tl_image[:, :, 0] = tli_r
            tl_image[:, :, 1] = tli_g
            tl_image[:, :, 2] = tli_b
            grayb = cv2.threshold(tli_b, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            histb = np.histogram(grayb, 256, (0, 255))[0]
            grayg = cv2.threshold(tli_g, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            histg = np.histogram(grayg, 256, (0, 255))[0]
            grayr = cv2.threshold(tli_r, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            histr = np.histogram(grayr, 256, (0, 255))[0]

            black, white = histb[0] + histg[0] + histr[0], histb[-1] + histg[-1] + histr[-1]
            gray = grayb & grayg & grayr \
                   if white > black else \
                   grayb | grayg | grayr

            clr_fpath = "data/ocr/clr-%s-%d.png"%(name, i)
            gry_fpath = "data/ocr/gry-%s-%d.png"%(name, i)
            cv2.imwrite(clr_fpath, tl_image)
            cv2.imwrite(gry_fpath, gray)
            text = pytesseract.image_to_string(Image.open(gry_fpath), config="-l chi_sim --oem 1 --psm 7")
            texts.append((topleftp, text))
        texts.sort(key=lambda i: i[0][1])
        return [i[1] for i in texts]

    def _prep(self, tl_image):
        ''' ocr 识别
        '''
        h, w = tl_image.shape
        zoomlevel = h/100 # 文本行高 100 像素
        gray = cv2.resize(tl_image, (int(w/zoomlevel), int(h/zoomlevel)))
        gray = cv2.bilateralFilter(gray, 13, 13, 13)

        tl_h, tl_w = gray.shape
        ocr_h, ocr_w = 400, tl_w+500 if tl_w > 500 else tl_w+1000
        ocr_image = np.ones((ocr_h, ocr_w))*gray.mean()
        ocr_image[int(ocr_h/2-tl_h/2):int(ocr_h/2+tl_h/2), int(ocr_w/2-tl_w/2):int(ocr_w/2+tl_w/2)] = gray

        return ocr_image
