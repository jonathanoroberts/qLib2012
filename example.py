####
# demonstration of qLib capabilities in psychopy
#

from psychopy import visual,event,core
import random
from qLib.qLib import *
#
#create a psychoPy window
myWin = visual.Window(fullscr=False,size=(800,600 ),winType='pyglet')

# and some stimuli to use with the questions
aPicture = visual.ImageStim(myWin, 'flatirons.png', pos = (0,.3), size=1.0)
someText =  visual.TextStim(myWin, text='Here is some text', alignHoriz = 'center', height=.1, color = 'blue', pos=(0,.5))

# create a text Stimulus for the instructions
# usable color names can be found at http://www.w3schools.com/html/html_colornames.asp
instructions = visual.TextStim(myWin, text='Examples of QLib "questions" follow.\nhit space to begin', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'navajowhite', pos=(0,0))

#draw the instructions to the off screen buffer
instructions.draw()
# flip the offscreen buffer to be onscreen
myWin.flip()
# wait for the space bar to be pressed
event.waitKeys(keyList=['space'])

# now the example questions
# see the QLib.py file for documentation

someText.setText('question fieldtype - textField')
print textField(window=myWin,drawList=[someText])
core.wait(.5)
print textField(window=myWin,label='Enter a number',text='3.2',labelColor='lightblue',drawList=[aPicture],pos=(0,-.5),fieldtype='float')
core.wait(.5)

someText.setText('question fieldtype - form')
print form(window=myWin,drawList=[someText])
core.wait(.5)
print form(window=myWin, drawList=[aPicture], fields = [ ['Subject ID', 'black', '', 7, 'string'], ['Pretest Score', 'black', '98.6', 5, 'float'], ['Age', 'black', None, 3, 'int'] ], pos = [0,-0.3] )
core.wait(.5)

someText.setText('question fieldtype - multiChoice')
print multiChoice(window=myWin,drawList = [someText],nextKey='space')
core.wait(.5)
print multiChoice(window=myWin,forceChoice=False,drawList = [aPicture], vPos=-0.4,labels = ['Mountains','Leaves','Sky','Ocean'])
core.wait(.5)

someText.setText('question fieldtype - choice')
myLabels = ['a','b','c','d','e']
print choice(window=myWin,drawList = [someText],nextKey='space')
core.wait(.5)
print choice(window=myWin,forceChoice=False, drawList = [aPicture], vPos=-0.4,labels = ['Fall','Winter','Spring','Summer'])
core.wait(.5)

someText.setText('question fieldtype - slider')
print slider(window=myWin,  drawList = [someText])
core.wait(.5)
print slider(window=myWin, forceChoice=False, sliderLoc = -0.6, drawList = [aPicture], limits = [-500,500], start=0, snap2labels=True ,snap2mouse=True , feedback=True, feedbackDigits=1, labels = ['less','','','','','about\nthe\nsame','','','','','more'])
core.wait(.5)

someText.setText('question fieldtype - scale')
print scale(window=myWin, drawList = [someText])
core.wait(.5)
print scale(window=myWin, forceChoice=False, drawList = [aPicture], nButtons = 7, scaleLoc=-.6, numberButtons=True, labels = ['less','or','more'])
core.wait(.5)


someText.setText('question fieldtype - bars')
print bars(window=myWin,drawList=[someText])
core.wait(.5)
#shrink the picture a bit for this question
aPicture.setSize(.7)
print bars(window=myWin,forceChoice=False,nBars=5,width=.7,height=.5,drawList=[aPicture], 
                    barColors=['red','white','white','white','blue'],labels=['a','b','c','d','e'],yLabels=['bottom','a pretty\nlong label','top'], defaultHeight=[20,30,40,50,60])
aPicture.setSize(1.0) # restore picture size
core.wait(.5)

someText.setText('question fieldtype - textInput\nminimal editing capability')
print textInput(window=myWin, drawList = [someText])
core.wait(.5)
print textInput(window=myWin, prompt = 'Please describe this picture', drawList = [aPicture], boxTop=-.4)
core.wait(.5)

print textDialog(window=myWin, caption='question fieldtype - textDialog\nThis type of text input is fully editable,\nbut does not allow a stimulus to be drawn.')
core.wait(.5)

# say thanks
thanks = visual.TextStim(myWin, text='Thanks for viewing these examples.', wrapWidth = 1.8, alignHoriz = 'center', height=.1, color = 'mediumturquoise', pos=(0,0))
thanks.draw()
myWin.flip()
# and wait 2 seconds before quitting
core.wait(2.0)
core.quit()



