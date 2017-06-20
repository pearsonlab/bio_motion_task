# Bio Motion P3
===========

Investigating the extent to which the reorienting or contextual updating of attention is modulated by biological motion.

This psychopy code implements a standard oddball task.

## Task Instructions:
- Participants should press the "down" key when they see green dots

### Brief Task Design:
- The task needs to be run in a minimum of 40 trial blocks for correct oddball proportions. Currently set at 240 trials (~15min).
- The oddball proportions are 30% targets, 70% non-targets.
- The stimuli are evenly split between biological motion and control motion (see script for making control stim for more info).
- The sequence is as follows: [1.8-2.2 sec Fixation cross (jittered)] -> [3 sec Stim Presentation] -> [0.5 sec ISI]

### Brief Predictions:
- There will be a difference between targets and non-targets in the P3b ERP component.
- This ERP difference will be modulated between biological motion and control targets.
- High gamma oscillatory activity will reveal further differences between biological and control motion.
