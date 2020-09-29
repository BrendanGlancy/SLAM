#!/usr/bin/env python3

import time
import cv2
import sdl2
import sdl2.ext
sdl2.ext.init()

W = 1920//2
H = 1080//2

disp = Display(W,H)
orb = cv2.ORB()

def process_frame(img):
    # keyPoint1 and descriptors1 detect and compute 
    kp1, des1 = orb.detectAndCompute(img1,None)

    img = cv2.resize(img, (W,H))
    disp.paint(img)


if __name__ == '__main__':
    cap = cv2.VideoCapture("test.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            process_frame(frame)
        else:
            break

