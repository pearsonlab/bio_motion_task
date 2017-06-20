from psychopy import core, visual
from psychopy.visual import ElementArrayStim

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
        
        # useful defaults for us (that are not defaults of ElementArrayStim)
        if 'elementMask' not in kwargs:
            kwargs['elementMask'] = 'circle'
            
        if 'sizes' not in kwargs:
            kwargs['sizes'] = 10
            
        
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
            self.dot_xys_temp = []
            for j in range(self.markers):
                point = name.loc[j+self.markers*i].tolist()
                self.dot_xys_temp.append([point[angle],point[2]])
            self.dot_xys.append(self.dot_xys_temp)
                        
        super(MotionDots, self).__init__(win, xys=self.dot_xys[0], **kwargs)

    def draw(self):
        """
        Draw the stim, then increment frame number.
        """
        
        self.current_frame = (self.current_frame + 1) % self.frames
        
        self.xys = self.dot_xys[self.current_frame]

        super(MotionDots, self).draw()   