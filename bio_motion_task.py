import sys
from psychopy import visual, core, event, gui
import json
import os
from os import listdir
from datetime import datetime
from os.path import isfile, join
import numpy as np

from utils import Flicker

options = ['Motion', 'Instrumental', 'Direction']

instrumental = ['Cycle', 'Paint', 'Saw', 'Sweep', 'Row', 'Drive']
global_motion = ['Crawl', 'Cycle', 'Walk', 'Row', 'Drive']
left_motion = ['Crawl_45L', 'Cycle_45L', 'Drive_45L',
                'Paint_45L', 'Row_45L', 'Walk_45L']

def play_movie(win, movie, timing, keymap, participant, trigger=None):
    mov = visual.MovieStim3(win, 'movies/'+movie, size=[1620,956.25],
                       flipVert=False, flipHoriz=False, loop=True, noAudio=True)

    timer = core.CountdownTimer(timing)
    mov_start = core.getTime()
    if trigger:
        trigger.flicker(1)
    event.clearEvents(eventType='keyboard')

    while mov.status != visual.FINISHED:
        mov.draw()
        win.flip()
        keys = event.getKeys()

        if keys:
            if 'escape' in keys:
                trigger.flicker_block(0)
                
                # Save end data
                t = datetime.now()
                day_time = '%d:%d:%d:%d' % (t.hour, t.minute, t.second, t.microsecond)
                end_time = globalTimer.getTime()
                save_data(day_time, end_time, participant)

                win.close()
                core.quit()
            elif 'left' == keys[0]:
                win.flip()
                win.flip()
                trigger.flicker_block(4)
                time_of_resp = core.getTime()
                return (mov_start, 'left', time_of_resp)
            elif 'right' == keys[0]:
                win.flip()
                win.flip()
                trigger.flicker_block(4)
                time_of_resp = core.getTime()
                return (mov_start, 'right', time_of_resp)
            elif 'down' == keys[0]:
                win.flip()
                win.flip()
                trigger.flicker_block(4)
                time_of_resp = core.getTime()
                return (mov_start, 'down', time_of_resp)
            else:
                win.flip()
                win.flip()
                trigger.flicker_block(16)
                time_of_resp = core.getTime()
                return (mov_start, 'invalid_resp', time_of_resp)
        if not keys:
            if timer.getTime() <= 0:
                win.flip()
                win.flip()
                trigger.flicker_block(16)
                return (mov_start, 'timeout', 'timeout')

def text_and_stim_keypress(win, text, participant, stim=None):
        if stim is not None:
            if type(stim) == list:
                map(lambda x: x.draw(), stim)
            else:
                stim.draw()
        display_text = visual.TextStim(win, text=text,
                                        font='Helvetica', alignHoriz='center',
                                        alignVert='center', units='norm',
                                        pos=(0, 0), height=0.1,
                                        color=[255, 255, 255], colorSpace='rgb255',
                                        wrapWidth=2)
        display_text.draw()
        win.flip()
        key = event.waitKeys()
        if key[0] == 'escape':
            # Save end data
            t = datetime.now()
            day_time = '%d:%d:%d:%d' % (t.hour, t.minute, t.second, t.microsecond)
            end_time = globalTimer.getTime()
            save_data(day_time, end_time, participant)

            core.quit()
            win.flip()
        win.flip()


def version(win, choice, participant):
    if choice == "Instrumental":
        text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person is moving on their own." +
                                "\n\n       -Press the LEFT arrow key if the person is using a tool or vehicle\n        in their motion.", participant)
        text_and_stim_keypress(win, "Ready?\n\n" +
                                'Press any key to begin!', participant)
    elif choice == "Motion":
        text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person could perform this \n        action in one spot." +
                                "\n\n      -Press the LEFT arrow key if the person would be moving in \n        a specific direction while performing this action.", participant)
        text_and_stim_keypress(win, "Ready?\n\n" +
                                'Press any key to begin!', participant)
    else:
        text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person is moving to the right." +
                                "\n\n      -Press the LEFT arrow key if the person is moving to the left."+
                                "\n\n      -Press the DOWN arrow key if the person is not moving\n        distinctly in either direction.", participant)
        text_and_stim_keypress(win, "Ready?\n\n" +
                                'Press any key to begin!', participant)

def play_through_movies(win, files, timing, keymap, choice, participant, delay, round, trigger):

    # For pseudo-random orders
    routes = [[13,  9, 10, 17, 35,  3, 31,  8, 32, 16,  5, 29, 34, 14,  0, 15, 27,
                11, 19, 22,  4, 18,  1, 26, 25, 28,  6, 12,  2, 30,  7, 33, 21, 24, 23, 20],
              [ 8, 24, 27,  9,  3, 22, 17, 12,  6, 26, 32, 15, 13,  1,  2, 19, 29,
                33, 21, 31, 34,  0, 20,  5, 10, 14, 23, 35, 18,  4,  7, 16, 25, 30, 11, 28],
              [15,  0, 30,  4,  3, 21, 32, 26,  6, 34, 14, 11, 19, 27, 31, 33, 16,
                20, 22, 28, 24, 35, 18, 10,  9,  8,  2,  1, 23, 25,  7, 17,  5, 29, 13, 12]]

    for i in routes[round]:
        file = files[i]
        mov_start, resp, time_of_resp = play_movie(win, file, timing, keymap, participant, trigger)

        win.flip()
        win.flip()

        trial = {}
        trial['mov_start'] = mov_start
        trial['response'] = resp
        trial['time_of_resp'] = time_of_resp

        if time_of_resp != 'timeout':
            trial['resp_time'] = time_of_resp - mov_start

        trial['action'] = file.strip('.mov')
        trial['trial_type'] = choice

        # Storing data for each trial type
        if choice == 'Instrumental':
            if file[:-8] in instrumental:
                trial['is_type'] = True
            else:
                trial['is_type'] = False
        elif choice == 'Motion':
            if file[:-8] in global_motion:
                trial['is_type'] = True
            else:
                trial['is_type'] = False
        else:
            if file[:-4] in left_motion:
                trial['is_type'] = True
            else:
                trial['is_type'] = False

        # Storing data for correct vs incorrect responses
        if resp != 'timeout':
            if trial['is_type'] == True:
                if resp == 'left':
                    trial['correct_resp'] = True
                else:
                    trial['correct_resp'] = False
            else:
                if choice == 'Direction':
                    if resp == 'right' and file[-5] == 'R':
                        trial['correct_resp'] = True
                    elif resp == 'down' and file[-5] != 'R':
                        trial['correct_resp'] = True
                    else:
                        trial['correct_resp'] = False
                else:
                    if resp == 'right':
                        trial['correct_resp'] = True
                    else:
                        trial['correct_resp'] = False
        else:
            trial['correct_resp'] = False

        if not os.path.exists('behavioral/'):
            os.makedirs('behavioral')

        with open('behavioral/bio_motion_task_'+ participant + '.json', 'a') as f:
            f.write(json.dumps(trial))
            f.write('\n')

        print i, trial['action'], trial['response'], trial['correct_resp']
        core.wait(delay)


def save_data(day_time, start_time, participant):

    info = {}
    info['wall_time'] = day_time
    info['psychopy_time'] = start_time

    if not os.path.exists('behavioral/'):
            os.makedirs('behavioral')

    with open('behavioral/bio_motion_task_'+ participant + '.json', 'a') as f:
        f.write(json.dumps(info))
        f.write('\n')

def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addText('Biological Motion Task', color="Blue")
    dlg.addField('Subject ID:', 'practice')
    dlg.addField('Movie Timing:', 10)
    dlg.addField('Delay:', 2)
    dlg.addField('Rounds:', 2)
    dlg.addField('Version','Direction', choices=options)
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()

def run():
    participant, timing, delay, rounds, choice = get_settings()

    keymap = {'left': 1, 'right': 0}

    # Define window
    win = visual.Window(winType='pyglet', monitor="testMonitor", units="pix", screen=1,
            fullscr=True, colorSpace='rgb255', color=(0, 0, 0))
    win.mouseVisible = False
    trigger = Flicker(win)

    # Instructions
    text_and_stim_keypress(win, "You are going to be observing a number of peoples performing different actions.\n\n" +
                                '(Press any key to continue)', participant)
    version(win, choice, participant)

    # Starting timers and save initial information
    global globalTimer
    globalTimer = core.Clock()
    start_time = globalTimer.getTime()
    t = datetime.now()
    day_time = '%d:%d:%d:%d' % (t.hour, t.minute, t.second, t.microsecond)
    save_data(day_time, start_time, participant)

    # Wait
    win.flip()
    core.wait(delay)
    win.flip()

    # Import movies
    files = [f for f in listdir('movies')
                if isfile(join('movies', f))
                if f.endswith('.mov')]

    # Play movies and save data
    rc = np.random.choice(3, 3, replace=False) #rc for round_choice

    if rounds > 0:
        # First round
        play_through_movies(win, files, timing, keymap,
                            choice, participant, delay, rc[0], trigger)

        if rounds > 1:

            # Remove already completed round
            options.pop(options.index(choice))
            next_rounds = options

            # Indices for random selection of next round
            next = np.random.choice(2, 2, replace=False)

            # Second round
            version(win, next_rounds[next[0]], participant)
            play_through_movies(win, files, timing, keymap,
                                next_rounds[next[0]], participant, delay, rc[1], trigger)
            if rounds > 2:

                # Third round
                version(win, next_rounds[next[1]], participant)
                play_through_movies(win, files, timing, keymap,
                                next_rounds[next[1]], participant, delay, rc[2], trigger)

    # Exit
    text_and_stim_keypress(win, "You're finished!\n\n" +
                                '(Press any key to exit)', participant)
    
    # Save end data
    t = datetime.now()
    day_time = '%d:%d:%d:%d' % (t.hour, t.minute, t.second, t.microsecond)
    end_time = globalTimer.getTime()
    save_data(day_time, end_time, participant)
    
    core.quit()

if __name__ == '__main__':
    run()
