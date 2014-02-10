####
# demo of qLib capabilities in psychopy
#

from psychopy import visual,event,core
import random
from qLib.qLib import *
from ctypes import *
class CGPoint(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float)
    ]
carbon = pyglet.lib.load_library(framework='/System/Library/Frameworks/Carbon.framework')

def set_mouse_position(win, x, y):
    point = CGPoint()
    point.x = ( ((x+1) / 2.0) * win.size[0] ) + win.pos[0]
    point.y = ( ((y-1) / -2.0) * win.size[1] ) + win.pos[1]
    carbon.CGWarpMouseCursorPosition(point)
    win.winHandle._mouse_x = point.x-win.pos[0]
    win.winHandle._mouse_y = point.y-win.pos[1]

def continuous(window=None, drawList=None, timeout=1.0):
    sliderLine = visual.ImageStim(myWin,image='qLib/sliderLine.png',units = 'norm', size=(1.6,0.02), pos=(0.0,-0.7))
    slider = visual.ImageStim(myWin,image='qLib/slider.png', units = 'norm', size = (.03,.07), pos=(0,-0.7))
    leftLabel = visual.TextStim(myWin, text='not intense at all', alignHoriz = 'left', height=0.05, color = 'black', pos=(-0.8,-0.75))
    rightLabel = visual.TextStim(myWin, text='the most intense possible', alignHoriz = 'right', height=0.05, color = 'black', pos=(0.8,-0.75))
    title = visual.TextStim(myWin, text='How intense is the current feeling?', alignHoriz = 'center', height=0.05, color = 'black', pos=(0.0,-0.65))
    set_mouse_position(window,0.0,-0.7)
    mouse = event.Mouse(win=window)
    mouse.setVisible(0)
    done = False
    rating = []
    timer=core.Clock()
    start=timer.getTime()
    window.flip()
    while not done:
        x,y = mouse.getPos()
        x = max(-0.8,min(0.8,x))
        slider.setPos([x,-0.7])
        rating.append( [ int( ( ( x+0.8 ) / 1.6 )*100),int(timer.getTime()*1000) ] )
        for item in drawList:
            item.draw()
            leftLabel.draw()
            rightLabel.draw()
            title.draw()
        sliderLine.draw()
        slider.draw()
        window.flip()
#        if timer.getTime() > start+timeout or mouse.getPressed()[0] != 0:
        if timer.getTime() > start+timeout:
            done = True
            mouse.setVisible(1)
    return rating

#
#create a psychoPy window
myWin = visual.Window(fullscr=False,size=(1024,768 ),winType='pyglet')

# and some stimuli to use with the question
aPicture = visual.ImageStim(myWin, 'flatirons.png', pos = (0,.3))
# create a text Stimulus for the instructions
# usable color names can be found at http://www.w3schools.com/html/html_colornames.asp
instructions = visual.TextStim(myWin, text='Demo of a continuous slider.\nhit space to begin then move the mouse', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'navajowhite', pos=(0,0))

#draw the instructions to the off screen buffer
instructions.draw()
# flip the offscreen buffer to be onscreen
myWin.flip()
# wait for the space bar to be pressed
event.waitKeys(keyList=['space'])

# continuous
data = continuous(myWin,[aPicture],timeout=3.0)
print data


# say thanks
thanks = visual.TextStim(myWin, text='sampled slider position and time were written to the console window.', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'mediumturquoise', pos=(0,0))
thanks.draw()
myWin.flip()
# and wait 1 seconds before quitting
core.wait(3.0)
core.quit()



