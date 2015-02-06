#
# demo of qLib with movie stimuli
#
from psychopy import visual,event,core
from qLib.qLib import *

#create a psychoPy window
myWin = visual.Window(fullscr=False,size=(1024,768 ),winType='pyglet')

mov = visual.MovieStim(myWin, 'testmovie.mp4', size=(.75,.75), pos=(0,.5),units='norm',flipVert=False,flipHoriz=False,)

# create a text Stimulus for the instructions
# usable color names can be found at http://www.w3schools.com/html/html_colornames.asp
instructions = visual.TextStim(myWin, text='Examples of QLib "questions" follow.\nhit space to begin', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'navajowhite', pos=(0,0))
#
#draw the instructions to the off screen buffer
instructions.draw()
# flip the offscreen buffer to be onscreen
myWin.flip()
# wait for the space bar to be pressed
event.waitKeys(keyList=['space'])
#
# now the example questions
# see the QLib.py file for documentation

print bars(window=myWin,forceChoice=False,nBars=5,width=.7,height=.5,drawList=[mov], labels=['a','b','c','d','e'],yLabels=['a pretty\nlong label'], defaultHeight=[20,30,40,50,60])
#print textInput(window=myWin, drawList = [someText])
#print textDialog(window=myWin, title='Feedback', caption='This type of text input is fully editable.\nWhat do you want to say?', initialText='enter your response here')
core.wait(.5)

# say thanks
thanks = visual.TextStim(myWin, text='Thanks for viewing this example.', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'mediumturquoise', pos=(0,0))
thanks.draw()
myWin.flip()
# and wait 1 seconds before quitting
core.wait(1.0)
core.quit()



