#!/usr/bin/env python
# coding: utf-8

from constant import *
from glob import glob
import cv2 as cv
import numpy as np
from card import Card
from canvas import Canvas

def match_temp(gray_im, temp_im, threshold=0.85):
    w, h = temp_im.shape[::-1]
    res = cv.matchTemplate(gray_im, temp_im, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return zip(*loc[::-1])

def nms(pts):
    #TODO(zhiding)
    pass

def corner_nms(pts):
    mx = 0
    my = 0
    n = 0
    for pt in pts:
        mx += pt[0]
        my += pt[1]
        n += 1
        break
    return int(mx / n), int(my / n)

def card_nms(pts):
    nhit = 0
    sel_pts = []
    for pt in pts:
        is_pass = True
        for sel_pt in sel_pts:
            if (abs(sel_pt[0] - pt[0]) <= THRES_PIXEL_CARD_NMS
                    and abs(sel_pt[1] - pt[1]) <= THRES_PIXEL_CARD_NMS):
                is_pass = False
                break
        if is_pass:
            sel_pts.append(pt)
            nhit += 1
    return sel_pts

def read_card(fpath):
    card_type = ""
    card_value = ""
    fname = fpath.split('/')[-1].split('.')[0]
    for t in CARD_TYPE_STRS:
        if t in fname:
            card_type = t
            break
    for v in CARD_VALUE_STRS:
        if v in fname:
            card_value = v
            break
    return t, v

class Puzzle:
    def __init__(self, img_path):
        self.im = cv.imread(img_path)
        self.im_gray = cv.cvtColor(self.im, cv.COLOR_BGR2GRAY)
        ###  init
        # canvas, layout, groups
        self.init()
        pass

    def init(self):
        self.locate_canvas()
        self.recognize_cards()

    def run(self):
        steps = []
        score = 0
        n_clear = 0
        while (n_clear < NUM_CARDS_IN_ROW * NUM_CARDS_IN_COL):
            sol = ""
            for name in CARD_SELECT_ORDER:
                cards = []
                if name not in self.groups:
                    continue
                for p in self.groups[name]:
                    c = self.layout[p[1]][p[0]]
                    if c.is_exist:
                        cards.append(c)
                for i in range(len(cards)):
                    for j in range(i+1, len(cards)):
                        sol = cards[i].remove(self.layout, cards[j].x, cards[j].y)
                        if sol:
                            cards[i].is_exist = False
                            cards[j].is_exist = False
                            n_clear += 2
                            score += cards[i].cost
                            steps.append('{} {} ({},{}), ({},{})'.format(cards[i].name, sol, cards[i].x, cards[i].y, cards[j].x, cards[j].y))
                            break
                    if sol:
                        break
                if sol:
                    break
            if not sol:
                print("Dead game, exit.")
                    #TODO
        for s in steps:
            print(s)

    def locate_canvas(self):
        temp_im = cv.imread(PATH_TOP_LEFT_CORNER, 0)
        x1, y1 = corner_nms(match_temp(self.im_gray, temp_im, THRES_LOC_CANVAS))
        temp_im = cv.imread(PATH_BTM_RIGHT_CORNER, 0)
        x2, y2 = corner_nms(match_temp(self.im_gray, temp_im, THRES_LOC_CANVAS))
        self.canvas_rect = [[x1, y1], [x2, y2]]
        self.canvas_im = self.im[y1:y2+temp_im.shape[1], x1:x2+temp_im.shape[0]]

    def recognize_cards(self):
        self.layout = [[Card() for i in range(NUM_CARDS_IN_ROW)] \
                                for j in range(NUM_CARDS_IN_COL)]
        self.groups = dict()
        nhit = 0
        for fpath in glob(PATH_CARD_TEMP_GLOB):
            temp_im = cv.imread(fpath, 0)
            pts = card_nms(match_temp(self.im_gray, temp_im, THRES_LOC_CARDS))
            card_type, card_value = read_card(fpath)
            card_name = '{}_{}'.format(card_type, card_value)
            self.groups[card_name] = []
            for pt in pts:
                px = round((pt[0] + CARD_HALF_WIDTH - self.canvas_rect[0][0]) / CARD_WIDTH) - 1
                py = round((pt[1] + CARD_HALF_HEIGHT - self.canvas_rect[0][1]) / CARD_HEIGHT)- 1
                self.layout[py][px] = Card(card_name, px, py, CARD_COST[card_type][card_value], True)
                self.groups[card_name].append([px, py])
            nhit += len(pts)
        assert nhit == NUM_CARDS_IN_ROW * NUM_CARDS_IN_COL, nhit

    def print_layout(self):
        print("++++++++")
        for j in range(NUM_CARDS_IN_COL):
            for i in range(NUM_CARDS_IN_ROW):
                print("{}".format(self.layout[j][i].name), end='\t')
            print("\n")
        print("++++++++")

# class Card:
#     def __init__(self, name="", x=0, y=-1, cost=-1, is_exist=False):
#         self.x = x
#         self.y = y
#         self.cost = cost
#         self.name = name
#         self.is_exist = True

def main():
    p = Puzzle('./mumu06.png')
    #p.print_layout()
    p.run()


if __name__ == '__main__':
    main()

