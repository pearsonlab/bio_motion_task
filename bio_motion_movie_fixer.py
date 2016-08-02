import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import argparse

def import_file(filename):
    name = pd.read_csv(filename,
                           delim_whitespace=True, skiprows=[0], encoding='utf-16',
                          header=None)
    return name

def movie_writer(Hz):
    FFMpegWriter = animation.writers['ffmpeg']
    writer = FFMpegWriter(fps=Hz, bitrate=1000)

    return writer
# 1000 and 200 work

def make_movie(writer, filename, name, orientation, frames, markers):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', axisbg='black')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    if orientation == 90:
        new_filename = filename.strip('.txt')+'_90R.mov'
    elif orientation == 270:
        new_filename = filename.strip('.txt')+'_90L.mov'
    elif orientation == 135:
        new_filename = filename.strip('.txt')+'_45R.mov'
    elif orientation == 225:
        new_filename = filename.strip('.txt')+'_45L.mov'
    elif orientation == 0:
        new_filename = filename.strip('.txt')+'_0MM.mov'
    else:
        raise ValueError('Orientation value does not match valid options')

    with writer.saving(fig, 'movies/'+new_filename, 200):
        for i in range(frames):
            x=[]
            y=[]
            z=[]

            for j in range(markers):
                point = name.loc[j+markers*i].tolist()
                x.append(point[0])
                y.append(point[1])
                z.append(point[2])

            ax.view_init(0, orientation)
            ax.scatter(x, y, z, c='white', depthshade=False)
            ax.set_xlim3d(-200, 200)
            ax.set_ylim3d(-200, 200)
            ax.set_zlim3d(-200, 200)
            ax.axis('off')
            writer.grab_frame()
            ax.cla()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Make higher resolution bio_motion videos")
    parser.add_argument('file',
                        help="File from which to produce movies"
                        )
    parser.add_argument('frames', type=int,
                        help="Number of frames (in text file)"
                        )
    #parser.add_argument('markers', type=int,
    #					help="Number of markers"
    #					)
    #parser.add_argument('Hz', type=int,
    #					help="Frames per second"
    #					)
    parser.add_argument('orientation', type=int,
                        help="Orientation: 90 for 90R, 270 for 90L, 135 for 45R, 225 for 45L"
                        )

    args = parser.parse_args()

    print args.file
    name = import_file(args.file)
    writer = movie_writer(30)
    make_movie(writer, args.file, name, args.orientation, args.frames, 13)

# Required arguments: file, orientation, frames, markers, Hz
