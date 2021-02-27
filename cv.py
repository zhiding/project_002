#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from glob import glob

#im = cv2.imread('./sample.jpeg')
im = cv2.imread('./mumu05.png')
#im = cv2.imread('./sample_p8.jpeg')

def locate(src_im, temp_im, threshold=0.98):
    src_gray = cv2.cvtColor(src_im, cv2.COLOR_BGR2GRAY)
    w, h = temp_im.shape[::-1]
    res = cv2.matchTemplate(src_gray, temp_im, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    nhit = 0
    avg_x = 0
    avg_y = 0
    for pt in zip(*loc[::-1]):
        avg_x += pt[0]
        avg_y += pt[1]
        nhit += 1
        print(pt[0], pt[1], nhit)
        break
    avg_x = int(avg_x / nhit)
    avg_y = int(avg_y / nhit)
    return avg_x, avg_y

def resize_card_temp():
    src_dir = './cards'
    for item in glob(src_dir + '/*.jpeg'):
        im = cv2.imread(item)
        im = cv2.resize(im, (94, 128))
        cv2.imwrite(item, im)

temp = cv2.imread('./mumu_topleft.png', 0)
x1, y1 = locate(im, temp)

temp = cv2.imread('./mumu_bottomright.png', 0)
x2, y2 = locate(im, temp)

crop_im = im[y1:y2+temp.shape[1], x1:x2+temp.shape[0]]
cv2.imwrite("tmp.jpg", crop_im)

#resize_card_temp()

def represent(src_im):
    card_temps = {}
    src_gray = cv2.cvtColor(src_im, cv2.COLOR_BGR2GRAY)
    nhit = 0
    for item in glob('./mumu_crop2/*.jpg'):
        print("=====", item, "=====")
        im = cv2.imread(item, 0)
        w, h = im.shape[::-1]
        res = cv2.matchTemplate(src_gray, im, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.90)
        pts = []
        out_im = src_im.copy()
        for pt in zip(*loc[::-1]):
            is_pass = True
            for sel_pt in pts:
                if abs(sel_pt[0] - pt[0]) <= 10 and abs(sel_pt[1] - pt[1]) <= 10:
                    is_pass = False
                    break
            if is_pass:
                pts.append(pt)
                nhit += 1
                print(pt[0], pt[1])
                cv2.rectangle(out_im, pt, (pt[0]+113, pt[1]+152), (0, 255, 0), 5)
                pos_x = round((pt[0]+57-x1) / 114) - 1
                pos_y = round((pt[1]+76-y1) / 152) - 1
                cv2.putText(out_im, "{}/{}".format(pos_x, pos_y), pt, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.imwrite(item.replace('mumu', 'mumu2'), out_im)

    print(nhit)


#represent(im)
#print(x1,y1,x2,y2)
#print(im.shape[1], im.shape[0])

im = cv2.imread('./crop.jpg')
im = cv2.resize(im, (1130, 912))

w = 113
h = 152

for i in range(6):
    for j in range(10):
        crop_im = im[i*h:(i+1)*h, j*w:(j+1)*w]
        print(i, j)
        cv2.imwrite('./mumu_crop/{}_{}.jpg'.format(i, j), crop_im)






