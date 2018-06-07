#!/usr/bin/python

import sys
import retro
import numpy as np
from os import listdir
from os.path import isfile, join, isdir, dirname, realpath
from PIL import Image


# find level maps here: http://info.sonicretro.org/Sonic_the_Hedgehog_(16-bit)_level_maps
mp = Image.open(dirname(realpath(__file__))+"/01.PNG")
mp.load()
level_map =np.array(mp.convert(mode='RGB'), dtype="uint8" )
hf = 10 # highlight factor

# https://stackoverflow.com/questions/5996881/how-to-limit-a-number-to-be-within-a-specified-range-python


def render(file):
    movie = retro.Movie(file)
    movie.step()
    env = retro.make(game=movie.get_game(), state=retro.STATE_NONE, use_restricted_actions=retro.ACTIONS_ALL)
    env.initial_state = movie.get_state()
    env.reset()
    frame = 0
    framerate = 10
    while movie.step():
        if frame == framerate:
            # env.render()
            frame = 0
        else:
            frame += 1

        keys = []
        for i in range(env.NUM_BUTTONS):
            keys.append(movie.get_key(i))
        _obs, _rew, _done, _info = env.step(keys)
        # print(_info);
        y = _info['y']
        x = _info['x']
        # level_map[ _info['y'], _info['x']] == np.array([255, 255, 255], dtype=np.uint8)
        # level_map[y:(y+8), x:(x+8)] = np.full((8,8,3),fill_value=255, dtype=np.uint8)
        # level_map[y:(y+8), x:(x+8)] =np.array(level_map[y:(y+8), x:(x+8)])**1.1
        highlight = [[[min(x[0][0]+hf,255), min(x[0][1]+hf,255), min(x[0][2]+hf,255)],
        [min(x[1][0]+hf,255), min(x[1][1]+hf,255), min(x[1][2]+hf,255)],
        [min(x[2][0]+hf,255), min(x[2][1]+hf,255), min(x[2][2]+hf,255)],
        [min(x[3][0]+hf,255), min(x[3][1]+hf,255), min(x[3][2]+hf,255)],
        [min(x[4][0]+hf,255), min(x[4][1]+hf,255), min(x[4][2]+hf,255)],
        [min(x[5][0]+hf,255), min(x[5][1]+hf,255), min(x[5][2]+hf,255)],
        [min(x[6][0]+hf,255), min(x[6][1]+hf,255), min(x[6][2]+hf,255)],
        [min(x[7][0]+hf,255), min(x[7][1]+hf,255), min(x[7][2]+hf,255)],
        ] for x in level_map[y:(y+8), x:(x+8)]]
        # highlight = [print(x) for x in level_map[y:(y+8), x:(x+8)]]
        # highlight = [x + hf for x in level_map[y:(y+8), x:(x+8)]]
        # print(highlight)
        level_map[y:(y+8), x:(x+8)] = highlight
        # print(level_map)
        # exit();
    env.close()

if isdir(sys.argv[1]):
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    c = 0
    for file in onlyfiles:
        if ".bk2" in file :
            print('playing', file)
            render(sys.argv[1]+file)
        if c % 5==0:
            lm = Image.fromarray(level_map)
            lm.save('levelmap.jpeg')
        c+=1
    lm.show()
else:
    print('playing', sys.argv[1])
    render(sys.argv[1])
    lm = Image.fromarray(level_map)
    # lm.save('levelmap.jpeg')
    lm.show()