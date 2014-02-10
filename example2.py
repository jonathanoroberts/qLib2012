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

# and some stimuli to use with the questions
aPicture = visual.ImageStim(myWin, 'flatirons.png', pos = (0,.3))
someText =  visual.TextStim(myWin, text='Here is some text', alignHoriz = 'center', height=.1, color = 'blue', pos=(0,.5))
sliderLine = visual.ImageStim(myWin,image='qLib/sliderLine.png',units = 'norm', size=(1.6,0.02), pos=(0.0,-0.7))
slider = visual.ImageStim(myWin,image='qLib/slider.png', units = 'norm', size = (.03,.07), pos=(0,-0.7))
leftLabel = visual.TextStim(myWin, text='not intense at all', alignHoriz = 'left', height=0.05, color = 'black', pos=(-0.8,-0.75))
rightLabel = visual.TextStim(myWin, text='the most intense possible', alignHoriz = 'right', height=0.05, color = 'black', pos=(0.8,-0.75))
title = visual.TextStim(myWin, text='How intense is the current feeling?', alignHoriz = 'center', height=0.05, color = 'black', pos=(0.0,-0.65))
# create a text Stimulus for the instructions
# usable color names can be found at http://www.w3schools.com/html/html_colornames.asp
instructions = visual.TextStim(myWin, text='Examples of QLib "questions" follow.\nhit space to begin', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'navajowhite', pos=(0,0))

#draw the instructions to the off screen buffer
instructions.draw()
# flip the offscreen buffer to be onscreen
myWin.flip()
# wait for the space bar to be pressed
event.waitKeys(keyList=['space'])

# continuous
data = continuous(myWin,[aPicture,leftLabel,rightLabel,title],timeout=3.0)
print data

# now the example questions
# see the QLib.py file for documentation
print textField(window=myWin,label='Enter a number',labelColor='lightblue',drawList=[aPicture],pos=(0,-.5),type='float')
core.wait(.5)

print bars(window=myWin,limits=[-10,10],height=1,nBars=5,width=.5,drawList=[someText], labels=['a','b','c','d','e'],barColors=['red','white','white','white','blue'],yLabels=['democrat','moderate','republican'], yLabelColors=['lightblue','white','pink'])
core.wait(.5)

# shrink the picture a little for the next question
aPicture.setSize(.7)
print bars(window=myWin,forceChoice=False,nBars=5,width=.7,height=.5,drawList=[aPicture], labels=['a','b','c','d','e'],yLabels=['a pretty\nlong label'], defaultHeight=[20,30,40,50,60])
core.wait(.5)

print textInput(window=myWin, drawList = [someText])
core.wait(.5)

print textDialog(window=myWin, caption='This type of text input is fully editable.\nWhat do you want to say?', initialText='enter your response here')
core.wait(.5)
print multiChoice(window=myWin,drawList = [someText], vPos=0.2,labels = ['Now is','the time for','all good','men to come','to the','aid','of their party'])
core.wait(.5)

#Example of how to use a list to randomly shuffle response options in multiple choice item.
myLabels = ['a','b','c','d','e']
random.shuffle(myLabels)

#To use data obtained from these functions, they must be given a label (e.g. item in line 48). Printing the function will simply return response/rt's in the output window.
#Here is an example of how you would really want to call these functions in an experiment
item = choice(window=myWin,drawList = [someText], vPos=0.2,labels = myLabels)
core.wait(.5)
print item, myLabels[item[0]]

#Here are some more functions
print slider(window=myWin, sliderLoc = -0.6, drawList = [someText], limits = [-500,500], start=0, snap2labels=True ,snap2mouse=True , feedback=True, feedbackDigits=1, labels = ['less','','','','','about\nthe\nsame','','','','','more'])
core.wait(.5)

print scale(window=myWin, drawList = [someText], nButtons = 7, scaleLoc=-.6, numberButtons=True, forceChoice = False, labels = ['less','or','more'])
core.wait(.5)

# say thanks
thanks = visual.TextStim(myWin, text='Thanks for viewing these examples.', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'mediumturquoise', pos=(0,0))
thanks.draw()
myWin.flip()
# and wait 1 seconds before quitting
core.wait(1.0)
core.quit()



