import sys
from psychopy import visual, core, event, gui
import json
import os
from os import listdir
from os.path import isfile, join
import numpy as np

from utils import flicker

options = ['Motion', 'Instrumental', 'Direction']

instrumental = ['Cycle', 'Paint', 'Saw', 'Sweep', 'Row', 'Drive']
global_motion = ['Crawl', 'Cycle', 'Walk', 'Row', 'Drive']
left_motion = ['Crawl_45L', 'Cycle_45L', 'Drive_45L',
				'Paint_45L', 'Row_45L', 'Walk_45L']

def play_movie(win, movie, timing, keymap):
	mov = visual.MovieStim3(win, 'movies/'+movie, size=[1620,956.25],
                       flipVert=False, flipHoriz=False, loop=True)
	
	timer = core.CountdownTimer(timing)
	mov_start = core.getTime()
	flicker(win, 1)
	event.clearEvents(eventType='keyboard')
	
	while mov.status != visual.FINISHED:
		mov.draw()
		win.flip()
		keys = event.getKeys()
		
		if keys:
			if 'escape' in keys:
				flicker(win, 0)
				win.close()
				core.quit()
			elif 'left' == keys[0]:
				win.flip()
				win.flip()
				flicker(win, 4)
				time_of_resp = core.getTime()
				return (mov_start, 'left', time_of_resp)
			elif 'right' == keys[0]:
				win.flip()
				win.flip()
				flicker(win, 4)
				time_of_resp = core.getTime()
				return (mov_start, 'right', time_of_resp)
			elif 'up' == keys[0]:
				win.flip()
				win.flip()
				flicker(win, 4)
				time_of_resp = core.getTime()
				return (mov_start, 'up', time_of_resp)
			else:
				win.flip()
				win.flip()
				flicker(win, 16)
				time_of_resp = core.getTime()
				return (mov_start, 'invalid_resp', time_of_resp)
		if not keys:
			if timer.getTime() <= 0:
				win.flip()
				win.flip()
				flicker(win, 16)
				return (mov_start, 'timeout', 'timeout')
	
def text_and_stim_keypress(win, text, stim=None):
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
			core.quit()
			win.flip()
		win.flip()


def version(win, choice):
	if choice == "Instrumental":
		text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person is moving on their own." +
								"\n\n       -Press the LEFT arrow key if the person is using a tool or vehicle\n        in their motion.")
		text_and_stim_keypress(win, "Ready?\n\n" +
								'Press any key to begin!')
	elif choice == "Motion":
		text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person could do this action\n        in one spot." +
								"\n\n      -Press the LEFT arrow key if the person would be moving around\n        while performing this action.")
		text_and_stim_keypress(win, "Ready?\n\n" +
								'Press any key to begin!')
	else:
		text_and_stim_keypress(win, "For THIS round...\n\nWHILE the movie is playing:\n\n      -Press the RIGHT arrow key if the person is moving to the right." +
								"\n\n      -Press the LEFT arrow key if the person is moving to the left."+
								"\n\n      -Press the UP arrow key if the person is not moving\n        in either direction.")
		text_and_stim_keypress(win, "Ready?\n\n" +
								'Press any key to begin!')	

def play_through_movies(win, files, timing, keymap, choice, participant, delay, round):
	
	# For pseudo-random orders
	routes = [[ 11, 8, 10,  5,  3,  6,  2, 15, 13, 17, 14, 12,  4,  0,  7,  9, 16, 1 ],
			  [ 7,  4, 17,  6,  1,  9,  0,  2, 12, 16, 11,  8,  5, 15, 10,  13, 3, 14],
			  [ 5,  3, 13,  9,  4, 12,  2,  0, 17,  8, 16,  1, 10, 15, 11, 14,  7, 6 ]]
			   
	for i in routes[round]: 
		file = files[i]
		mov_start, resp, time_of_resp = play_movie(win, file, timing, keymap) 
		
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
					elif resp == 'up' and file[-5] != 'R':
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
	info['day_time'] = day_time
	info['start_time'] = start_time
	
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
    dlg.addField('Delay:', 3)
    dlg.addField('Rounds:', 3)
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
	
	# Instructions
	text_and_stim_keypress(win, "You are going to be observing a number of peoples performing different actions.\n\n" +
								'(Press any key to continue)')
	version(win, choice)
	
	# Starting timers and save initial information
	globalTimer = core.Clock()
	start_time = globalTimer.getTime()
	day_time = core.getAbsTime()
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
							choice, participant, delay, rc[0])
		
		if rounds > 1:
		
			# Remove already completed round
			options.pop(options.index(choice))
			next_rounds = options
			
			# Indices for random selection of next round
			next = np.random.choice(2, 2, replace=False)
	
			# Second round
			version(win, next_rounds[next[0]])
			play_through_movies(win, files, timing, keymap, 
								next_rounds[next[0]], participant, delay, rc[1])
			if rounds > 2:
				
				# Third round
				version(win, next_rounds[next[1]])
				play_through_movies(win, files, timing, keymap, 
								next_rounds[next[1]], participant, delay, rc[2])
	
	# Exit		
	text_and_stim_keypress(win, "You're finished!\n\n" +
								'(Press any key to exit)')
	core.quit()
	
if __name__ == '__main__':
	run()