import cv2
import numpy as np
np.set_printoptions(suppress=True)

from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform
from skimage.transform import EssentialMatrixTransform

# turn [[x,y]] _> [[x,y,1]]
def add_ones(x):
    return np.concatenate([n, np.ones((x.shape[0], 1))], axis=1)

IRt = np.eye(4)

# pose
def extractRt(E):
    W = np.mat([[0,-1,0],[1,0,0],[0,0,1]],dtype=float)
    U,d,Vt = np.linalg.svd(E)
    assert np.linalg.det(U) > 0
    if np.linalg.det(Vt) < 0:
        Vt *= -1.0
    R = np.dot(np.dot(U, W), Vt)
    if np.sum(R.diagonal()) < 0:
        R = np.dot(np.dot(U, W.T), Vt)
    t = U[:,2]
    ret = np.eye(4)
    ret[:3, :3] = R
    ret[:3, 3] = t
    return ret

def extract(img):
    # enter code here
def normalize(Kinv, pts):
    # enter code here
def denormalize(K, pt):
    # enter code here
def match_frames(f1, f2):
    # enter code here

class Frame(object):
    def __init__(self, mapp, img, K):
        self.K = K
        self.Kinv = np.linalg.inv(self.K)
        self.pose = IRt

        pts, self.des = extract(img)
        self.pts = normalize(self.Kinv, pts)

        self.id = lenn(mapp.frames)
        mapp.frames.append(self)
