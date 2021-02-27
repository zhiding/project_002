#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy

class Card:
    def __init__(self, name='', x=-1, y=-1, cost=-1, is_exist=False):
        self.name = name
        self.x = x
        self.y = y
        self.cost = cost
        self.is_exist = is_exist

    def is_blocked(self):
        return self.is_exist

    def is_horizon(self, layout, px):
        if (px == self.x):
            return False
        sol = True
        for mx in range(min(px, self.x)+1, max(px, self.x)):
            my_card = layout[self.y][mx]
            if my_card.is_blocked():
                sol = False
        return sol

    def is_vertical(self, layout, py):
        if (py == self.y):
            return False
        sol = True
        for my in range(min(py, self.y)+1, max(py, self.y)):
            my_card = layout[my][self.x]
            if my_card.is_blocked():
                sol = False
        return sol

    def is_turn_once(self, layout, px, py):
        if (px == self.x and py == self.y):
            return False
        if (py == -1 or py == len(layout)):
            if self.is_vertical(layout, py):
                return True
        elif (px == -1 or px == len(layout[0])):
            if self.is_horizon(layout, px):
                return True
        else:
            corner_card = layout[py][self.x]
            if not corner_card.is_blocked():
                if (corner_card.is_vertical(layout, self.y) and corner_card.is_horizon(layout, px)):
                    return True
            corner_card = layout[self.y][px]
            if not corner_card.is_blocked():
                if (corner_card.is_horizon(layout, self.x) and corner_card.is_vertical(layout, py)):
                    return True
        return False

    def is_turn_twice(self, layout, px, py):
        if (px == self.x and py == self.y):
            return False
        # check turn_once + is_horizon
        for mx in range(-1, len(layout[0])+1):
            one_card = layout[py][px]
            if (mx+1) * (mx-len(layout[0])) == 0 or (not layout[py][mx].is_blocked()):
                if (self.is_turn_once(layout, mx, py) and one_card.is_horizon(layout, mx)):
                    return True
        # check turn_once + is_vertical
        for my in range(-1, len(layout)+1):
            one_card = layout[py][px]
            if (my+1) * (my-len(layout)) == 0 or (not layout[my][px].is_blocked()):
                if (self.is_turn_once(layout, px, my) and one_card.is_vertical(layout, my)):
                    return True
        return False

    def remove(self, layout, px, py):
        if self.y == py and self.is_horizon(layout, px):
            return "is_horizon"
        if self.x == px and self.is_vertical(layout, py):
            return "is_vertical"
        if self.is_turn_once(layout, px, py):
            return "is_turn_once"
        if self.is_turn_twice(layout, px, py):
            return "is_turn_twice"
        return ""


