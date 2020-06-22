import matplotlib.pyplot as plt
import math
import numpy as np
from cherab.mastu.machine import *

radians = 3.14159265 / 180.0

start = [1.50569999217987, -0.399749994277954]

angles = [  -0.391012817621231,
            -0.377983331680298,
            -0.365014135837555,
            -0.352100670337677,
            -0.339238584041595,
            -0.326423466205597,
            -0.313651055097580,
            -0.300917148590088,
            -0.288217544555664,
            -0.275548070669174,
            -0.262904673814774,
            -0.250283271074295,
            -0.237679839134216,
            -0.225090354681015,
            -0.212510809302330,
            -0.199937224388123,
            -0.187365636229515,
            -0.174792051315308,
            -0.162212505936623,
            -0.149623006582260,
            -0.137019574642181,
            -0.124398179352283,
            -0.111754782497883,
            -0.0990853235125542,
            -0.0863857045769692,
            -0.0736517906188965,
            -0.0608793906867504,
            -0.0480642840266228,
            -0.0352021791040897,
            -0.0222887266427279,
            -0.00931951310485601,
            0.00364970066584647]

def endpoint(start, angle, length):

    endx = start[0] - length * np.cos(angle)
    endy = start[1] + length * np.sin(angle)

    return [endx, endy]

fibre_r_z=[endpoint(start, a, 2.) for a in angles]

class fibres:
    """
    Geometry data for fibre bundles
    """

    def __init__(self):
        self.loaded = -1
        self.set_bundle(group=1)

    def set_bundle(self, group=None, fibre=12):
        if group == 1:
            self.group = 1
            self.load_ROV(fibre)
            self.numfibres = 14
            self.loaded = 1

    def set_fibre(self, number=1):
        self.set_bundle(group = self.group, fibre=number)

    def load_ROV(self,fibre):
        self.origin = self.machine_coordinates(*start, 180)
        if fibre in range(len(fibre_r_z)):
            self.term = self.machine_coordinates(*fibre_r_z[fibre], 180)

        self.distance = self.fibre_distance_world(-1)

    def machine_coordinates(self,R,Z,phi):
        return ( R * math.cos(phi * radians), R * math.sin(phi * radians), Z )

    def xhat(self):
        return (self.term[0]-self.origin[0]) / self.distance

    def yhat(self):
        return (self.term[1]-self.origin[1]) / self.distance

    def zhat(self):
        return (self.term[2]-self.origin[2]) / self.distance

    def fibre_distance_world(self,world):
        return np.sqrt( (self.origin[0]-self.term[0])**2 + (self.origin[1]-self.term[1])**2 + (self.origin[2]-self.term[2])**2)
