#!/usr/bin/env python3

import time
import cv2
import sdl2.ext

W = 1920//2
H = 1080//2

#pygame.init()
#display = pygame.display.set_mode((W,H))
#surface = pygame.Surface((W, H)).convert()

sdl2.ext.init()

windown = sld2.ext.Window("Slam", size=(640, 480))
window.show()

def process_frame(img):
    img = cv2.resize(img, (W,H))
    cv2.imshow('image', img)

    #surface.blit(img.swapaxes(0,1))
    print(img.shape)
    print(img)

    """
    pygame.pixelcopy.array_to_surface(surface,img,swapaxes(0,1))
    pygame.draw.circle(display, (255,0,0), (10,10),5, 1)
    display.blit(surface, (0,0))
    pygame.display.update()
    """


   # print(img.shape)

if __name__ == '__main__':
    cap = cv2.VideoCapture("test.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            process_frame(frame)
        else:
            break

