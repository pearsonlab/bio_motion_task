from psychopy import core, visual
from psychopy.visual.circle import Circle
from psychopy.visual.elementarray import ElementArrayStim
import pandas as pd
import numpy as np

class Flicker(Circle):
    """
    Creates a flickering circle in the upper right corner of the screen.
    This is to be used as a timing marker by a photodiode.
    The presence or absence of the circle marks out an 8-bit binary pattern,
    flanked at the beginning and end by a 1 (e.g., 5 is 1000001011).
    """
    def __init__(self, win, radius=0.04, pos=(0.84, 0.44), **kwargs):
        self.win = win
        self.bitpattern = None
        self.counter = None
        self.timer = core.MonotonicClock()

        kwargs['radius'] = radius
        kwargs['pos'] = pos

        # we want to override these
        kwargs['fillColorSpace'] = 'rgb255'
        kwargs['lineColorSpace'] = 'rgb255'
        kwargs['lineColor'] = None
        kwargs['units'] = 'height'
        kwargs['autoDraw'] = True

        super(Flicker, self).__init__(win, **kwargs)

    def flicker(self, code):
        """
        Start the flicker. code is an integer between 0 and 255 (=2^8).
        Calling this again before the sequence has finished will
        restart the flicker.
        """
        # convert to binary, zero pad to 8 bits, and add stop and start bits
        self.bitpattern = '1{:08b}1'.format(code)
        self.counter = 0

    def flicker_block(self, code):
        """
        Blocking version of flicker. The entire task will pause until the flicker is done. Returns the time of execution of the function.

        This is not best practice, but can be used in code that does not
        run a single event loop where flicker can be used.
        """
        start_time = self.timer.getTime()
        self.flicker(code)
        while self.bitpattern:
            self.win.flip()
        end_time = self.timer.getTime()

        return end_time - start_time

    def draw(self):
        """
        Draw the circle. Change its color based on the bitpattern and forward
        to the draw method for the circle.
        """
        if self.bitpattern:
            # if we've reached the end of the pattern
            if self.counter >= len(self.bitpattern):
                self.bitpattern = None
                self.fillColor = self.win.color
            else:
                if self.bitpattern[self.counter] == '1':
                    self.fillColor = (255, 255, 255)
                else:
                    self.fillColor = (0, 0, 0)

                # increment position in bit pattern
                self.counter += 1

        super(Flicker, self).draw()
      
class MotionDots(ElementArrayStim):
    """
    Creates a biological motion dot pattern corresponding to a movie frame.
    The draw method repeats frames indefinitely.
    """
    def __init__(self, win, moviename, angle, **kwargs):
        self.win = win
        self.moviename = moviename
        self.current_frame = 0
        self.angle = angle
        #self.colorSpace='rgb',
        
        # useful defaults for us (that are not defaults of ElementArrayStim)
        if 'elementMask' not in kwargs:
            kwargs['elementMask'] = 'circle'
            
        if 'sizes' not in kwargs:
            kwargs['sizes'] = 10
            
        if 'colorSpace' not in kwargs:
            kwargs['colorSpace'] = 'rgb'
            
        
        # load data from disk
        name = pd.read_csv(self.moviename+'.txt',
                              delim_whitespace=True, skiprows=[0], encoding='utf-16',
                              header=None)

        header = pd.read_csv(self.moviename+'.txt',
                             delim_whitespace=True, nrows = 1, encoding='utf-16',
                             header=None)

        # get movie attributes
        self.frames = header.iloc[0][2]
        self.markers = header.iloc[0][5]
        self.dot_xys=[]  # positions

        # load in data
        for i in range(self.frames):
            dot_xys_temp = []
            for j in range(self.markers):
                point = name.loc[j+self.markers*i].tolist()
                dot_xys_temp.append([point[angle],point[2]])
            self.dot_xys.append(dot_xys_temp)        
        #if 'xys' not in kwargs:
        kwargs['nElements'] = self.markers
        kwargs['xys'] = self.dot_xys[0]
        #kwargs['colorSpace'] = 'rgb'
        #kwargs['colors'] = dot_color
        
        #self.setColors(dot_color)
        
        super(MotionDots, self).__init__(win, **kwargs)

    def draw(self):
        """
        Draw the stim, then increment frame number.
        """
        
        self.current_frame = (self.current_frame + 1) % self.frames
        
        self.xys = self.dot_xys[self.current_frame]

        super(MotionDots, self).draw()            