#!/usr/bin/env python3

import time
import cv2
from display import Display
from frame import Frame, denormalize, match_frames, IRt
import numpy as np
import g20

import OpenGL.GL as gl
import pangolin

# camera intrinsics
W, H = 1920//2, 1080//2

F = 270
K = np.array([F,0,W//2],[0,F,H//2],[0,0,1]])

from multiprocessing import Process, Queue

class Map(object):
    def __init__(self):
        self.frames = []
        self.points = []
        self.state = None
        self.q = Queue()

        p = Process(target=self.viewer_thread, arg=self.q))
        p.daemon = True
        p.start()

    def viewer_thread(self, q):
        self.viewer_init()
        while 1:
            self.viewer_refresh(q)

    def viewer_init(self):
        pangolin.CreateWindowAndBind('Main', 640, 480)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.scam = pangolin.OpenGlRenderState( pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
                      pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY))
        self.handler = pangolin.Handler3D(self.scam)

        # Creat Interactive View in Window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
        self.dcam.SetHandler(self.handler)

    def viewer_refresh(self, q):
        if self.state is None or not q.empty():
            self.state = q.get()

        # turn state into points
        ppts = np.array([d[:3, 3] for d in self.state[0]])
        spts = np.array(self.state[1])

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.dcam.Activate(self.scam)

        gl.glPointSize(10)
        gl.glColor3f(0.0, 1.0, 0.0)
        pangolin.DrawPoints(ppts)

        gl.glPointSize(2)
        gl.glColor3f(0.0, 1.0, 0.0)
        pangolin.DrawPoints(spts)

        pangolin.FinishFrame()

    def display(self):



