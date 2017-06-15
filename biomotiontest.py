from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding
from utils import Flicker
import random
import pandas as pd

# Setup the Window
win = visual.Window(size=(1440, 900), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='height')

# Initialize components for Routine "trial"
continueRoutine = True

x = 0

motion = ['Chop','Crawl','Drive','Peddle','Playpool','Row','Saw','Stir','Sweep','Playtennis','Walk',
                'Cycle','Drink','Jump','Mow','Paint','Pump','Salute','Spade','Wave']

random = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
            21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
 
if random[x] > 10:
    angle = 1
if random[x] < 11:
    angle = 0

file = motion[random[x]]

name = pd.read_csv(file+'.txt',
                           delim_whitespace=True, skiprows=[0], encoding='utf-16',
                          header=None)
                        
header = pd.read_csv(file+'.txt',
                           delim_whitespace=True, nrows = 1, encoding='utf-16',
                          header=None)
                       
frames = header.iloc[0][2]
markers = header.iloc[0][5]
w=0
dot_xys=[] 

for i in range(frames):
    dot_xys_temp = []
    for j in range(markers):
        point = name.loc[j+markers*i].tolist()
        dot_xys_temp.append([point[angle],point[2]])
    dot_xys.append(dot_xys_temp)

dot_stim = visual.ElementArrayStim(
    win=win,
    units="pix",
    nElements=markers,
    elementTex=None,
    elementMask="circle",
    xys=dot_xys[w],
    sizes=10,
    colors=(255,0,0), 
    colorSpace='rgb',
    opacities=1.0
)

while continueRoutine > 0:
    for play in range(frames):
        dot_stim.xys = dot_xys[play]
        dot_stim.draw()
        win.flip()
