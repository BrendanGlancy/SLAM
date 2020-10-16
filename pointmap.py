from multiprocessing import Process, Queue
from frame import poseRt
import time
import numpy as np
import OpenGL.GL as gl
import pangolin
import g20

LOCAL_WINDOW = 20


class Point(object):
    # A point is a 3-D point in the world
    # Each point is observed in multiple Frames

    def __init__(self. mapp, loc):
        self.pt = loc
        self.frames = []
        self.idxs = []
        self.color = np.copy(color)

        self.id = mapp.max_point
        mapp.max_point += 1
        mapp.points.append(self)

    def homogeneous(self):
        return np.array([self.pt[0], self.pt[1], self.pt[2], 1.0])

    def orb(self):
        # TODO: average the orbs in hamming space
        des = []
        for f in self.frames:
            des.append(f.des[f.pts.index(self)])
        return des

    def delete(self):
        for f in self.frames:
            f.pts[f.pts.index(self)] = None
        del self

    def add_observation(self, frame, idx):
        frame.pts[idx] = self
        self.frames.append(frame)
        self.idx.append(idx)

class Map(object):
    def __init__(self):
        self.frame = []
        self.points = []
        self.max_point = 0
        self.state = None
        self.q = None

    # optimizer
    
    def optimize(self,local_window=LOCAL_WINDOW, fix_points=False, verbose=False):
        # create g20 optimizer
        opt = g20.SparseOptimizer()
        solver = g2o.BlockSovlerSE3(g20.LinearSolverCholmodSE3())
        solver = g20.OptimizerAlgorithLevenberg(solver)
        opt.set_algorithm(solver)

        robust_kernal = g20.RobustKernalHuber(n.sqrt(5.991))

        if local_window is None:
            local_frames = self.frames
        else:
            local_frames =self.frames[-local_window:]

        # add frames to graph
        for f in self.frames:
            pose = np.linalg.inv(f.pose)
            sbacam = g2o.SBACam(g2o.SE3Quat(pose[0:3, 0:3], pose[0:3, 3]))
            sbacam.set_cam(f.K[0][0], f.K[1][1], f.K[0][2], f.K[1][2], 1.0)

            v_se3 = g2o.VertexCam()
            v_se3.set_id(f.id)
            v_se3.set_estimate(sbacam)
            v_se3.set_fixed(f.id <= 1 or f not in local_frames)
            opt.add_vertex(v_se3)
            
        # add points to frames
        PT_ID_OFFSET = 0x10000
        for p in self.points:
            if not any([f in local_frames for f in p.frames]):
                continue

            pt = g20.VertexSBAPointXYZ()
            pt.set_estimate(p.pt[0:3])
            pt.set_marginalized(True)
            pt.set_fixed(fix_points)
            opt.add_vertex(pt)

            for f in p.frames:

    def display(self):
        if self.q is None:
            return
        poses, pts = [], []
        for f in self.frames:
            poses.append(f.pose)
        for p in self.points:
            pts.append(p.pt)
        self.q.put((np.array(pose), np.array(pts)))



