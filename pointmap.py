import numpy as np
import OpenGL.GL as gl
import pangolin

from multiprocessing import Processm Queue

class Point(object):
    # A point is a 3-D point in the world
    # Each point is observed in multiple Frames

    def __init__(self. mapp, loc):
        self.pt = loc
        self.frames = []
        self.idxs = []

        self.id = len(mapp.points)
        mapp.points.append(self)

    def add_observation(self, frame, idx):
        frame.pts[idx] = self
        self.frames.append(frame)
        self.idx.append(idx)

class Map(object):
    def __init__(self):
        self.frame = []
        self.points = []
        self.state = None
        self.q = None

    def create_viewer(self):
        self.q = Queue()
        self.vp = Process(target=self.viewer_thread, args=(self.q,))
        self.vp.daemon = True
        self.vp.start()

    def viewer_init(self, w, h):
        pangolin.CreateWindowAndBind('Main', w, h)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.scam = pangolin.OpenGIRenderState(
                pangolin.ProjectionMatrix(w, h, 420, 420, w//2, h//2, 0.2, 10000),
                pangolin.ModelViewLookAt(0, -10, -8,
                                         0, 0, 0,
                                         0, -1, 0))
        self.handler = pangolin.Handler3D(self.scam)

        # Create Interactive View in Window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -w/h)
        self.dcam.SetHandler(self.handler)

    def viewer_refresh(self, q):
        if self.state is None or not q.empty():
            self.state = q.get()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.dcam.Activate(self.scam)

        # Draw poses 
        gl.glColor3f(0.0, 1.0, 0.0)
        pangolin.DrawCameras(self.state[0])

        # draw keypoints
        gl.glPointSize(2)
        gl.glColor3f(1.0, 0.0, 0.0)
        pangolin.DrawPoints(self.state[1])

        pangolin.FinishFrame()

    def display(self):
        if self.q is None:
            return
        poses, pts = [], []
        for f in self.frames:
            poses.append(f.pose)
        for p in self.points:
            pts.append(p.pt)
        self.q.put((np.array(pose), np.array(pts)))



