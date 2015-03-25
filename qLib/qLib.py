__version__ = 'version 2.23'
''' QLib - CLIPR PsychoPy questionnaire library
Author:
Jonathan O. Roberts (with help from CLIPR TAs Katie Wolsiefer and Holen Katz)
Computer Laboratory for Instruction in Psychological Research
Department of Psychology and Neuroscience
University of Colorado Boulder
'''

import time,glob,random
from psychopy import visual,event,core
import pyglet
import wx, re
import os
pngPath = os.path.dirname(__file__)+'/'

class TextEntryDialog(wx.Dialog):
    def __init__(self, parent, title, caption, size, initialText=None, select=None, readOnly = False):
        style =  wx.STAY_ON_TOP | wx.RESIZE_BORDER
        try:
            super(TextEntryDialog, self).__init__(parent, -1, title, style=style)
        except:
            global app
            app = wx.PySimpleApp()
            super(TextEntryDialog, self).__init__(parent, -1, title, style=style)
        text = wx.StaticText(self, -1, caption)
        if readOnly:
            input = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE+wx.TE_READONLY)
        else:
            input = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        input.SetInitialSize(size)
        input.SetValue(initialText)
        if select:
            input.SetSelection(-1,-1)
        else:
            if not readOnly:
                input.SetInsertionPointEnd()
#        buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        buttons = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 5)
        sizer.Add(input, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(buttons, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizerAndFit(sizer)
        self.input = input
        self.Center()
    def setValue(self, value, select=True):
        self.input.SetValue(value)
        if select:
            self.input.SetSelection(-1,-1)
        else:
            self.input.SetInsertionPointEnd()
    def getValue(self):
        return self.input.GetValue()
    def show(self):
        self.SetEscapeId(wx.ID_NONE)
        if self.ShowModal() == wx.ID_OK:
            response = self.getValue()
            self.setValue('')
            return response
        else:
            print 'problem with textDialog...'
            return 'error'
    
def textDialog(window, clock=None,
                         wsize=(.8,.5),
                         caption='',
                         initialText='enter text here',
                         select=None,
                         readOnly = False):
    """Present a trial with a pop-up box that allows for text entry. Once text exceeds the entry window size, scrolling is enabled.
        allows for specification of pop-up size, static text (i.e. a question) that remains above the entry window, and initial text within
        the entry window (which can be replaced upon entry of text, or not).
    
    Keyword arguments:
        window -- The parent window within which the slider is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        wsize -- 
        title -- 
        caption -- Static text that appears above the text entry window
        initialText-- text that is initially displayed in the entry window. This can be edited by the participant
        select -- if True, initialText is highlighted when the trial is executed.  If False, initailText is not highlighted and the cursor begins after initialText (default = True)
        readOnly -- If True,subject cannot enter text in the window (usefull for presenting scrolling text), When readOnly is true, select is False by default"
                                to that position. If False, the subject must click and drag the slider to
                                change the value. (default False)
        size -- 
    
"""
    if select == None:
        if readOnly:
            select = False
        else:
            select = True
    size = (window.size[0] * wsize[0], window.size[1] * wsize[1])
    if not clock:
        clock = core.Clock()
    dlg = TextEntryDialog(None,title = '',caption=caption,readOnly = readOnly, initialText=initialText,select=select,size=size)
    window.flip()
    startTime = clock.getTime()
    response = dlg.show()
    rt = clock.getTime() - startTime
    window.flip()
    dlg.Destroy()
    return response, rt

def rbClicked(x = None, y = None, object = None, extendRight=False):
    """ Check to see if the click location (x,y) is within the bounds of object
    """
    left = object.pos[0] - (object.size[0]/2)
    right = object.pos[0] + (object.size[0]/2)
    if extendRight: right += .5
    top = object.pos[1] + (object.size[1]/2)
    bottom = object.pos[1] - (object.size[1]/2)

    if x < right and x > left and y < top and y > bottom:
        return True
    else:
        return False


def slider(window,clock = None,
                drawList = [],
                width = 0.8,
                limits = [0, 100],
                start = None,
                labels = ['left', 'right'],
                snap2mouse = False,
                snap2labels = False,
                feedback = False,
                feedbackDigits = 2,
                feedbackColor = 'lightblue',
                labelColor = 'white',
                sliderLoc = -0.7,
                forceChoice = True):
    """ Present a trial with a slider for response. The subject  can move the slider back and forth,
    with or without feedback, and then selects a value by clicking the Next button. Returns the
    value of the slider when the Next button is clicked.
    
    Keyword arguments:
        window -- The parent window within which the slider is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        width -- The width of the slider relative to the window (default 0.8 or 80% of the window width)
        limits -- A list containing the min and max values to be returned by the slider (default [0,100])
        start -- starting position in the units defined in "limits" ( default = None, will be calculated to be the middle)
        labels -- A list with the labels to be placed evenly spaced between the ends of the slider (default ['left', 'right'])
        snap2mouse -- If True, then the subject may click anywhere on the slider line and the slider will "snap"
                                to that position. If False, the subject must click and drag the slider to
                                change the value. (default False)
        snap2labels -- If True, slider motion is constrained to the label positions. (default False)
        feedback -- If True, then the current value is displayed while the slider is being moved (default False)
        feedbackDigits -- Precision of the feedback number, i.e. number of digits to the right of the decimal (default 2)
        feedbackColor -- Color of the feedback number (default 'lightblue')
        labelColor -- Color of the label text (default 'white')
        sliderLoc -- vertical position in norm units (-1 to +1) of the slider (default -0.7)
        forceChoice -- if True, requires the participant to click the slider before the next button is made visible
    """
    def drawAll():
        """ Draw all the objects that make up a slider trial """
        for item in drawList:
            item.draw()
        sliderLine.draw()
        slider.draw()
        if forceChoice == False or clickFirst == True:
            next.draw()
        for label in labelStims:
            label.draw()
     
     # create a clock if one is not provided
    if not clock:
        clock = core.Clock()

    def val2pos(val=None):
        range = float(limits[1]-limits[0])
        left = -( sliderLine.size[0] / 2 )
        return ( ( ( val - limits[0] ) / range ) * sliderLine.size[0] ) + left
        
    def pos2val(pos=None):
        range = limits[1]-limits[0]
        left = -( sliderLine.size[0] / 2 )
        return ( ( ( pos - left) / sliderLine.size[0] ) * range ) + limits[0]
        
    if start == None:
        start = limits[0] + ( ( limits[1] - limits[0] ) / 2.0 )

    sliderLine = visual.ImageStim(window,image=pngPath+'sliderLine.png',units = 'norm', size=(width*2.0,0.02), pos=(0.0,sliderLoc))
    slider = visual.ImageStim(window,image=pngPath+'slider.png', units = 'norm', size = (.03,.07), pos=(val2pos(start),sliderLoc))

    # Build a list containing the label stimuli. Calculate the positions for the labels so they are evenly spaced from end to end
    labelStims = []
    intervals = len(labels)-1
    if intervals == 0:      # If only one label was given, position it in the middle
        labelStims.append(visual.TextStim(window,units = 'norm', text=labels[0], color=labelColor, height=0.05, pos=(0,sliderLoc-0.05)))
    else: 
        spacing = (width*2)/intervals
        count = 0
        for label in labels:
            pos = -width + (spacing * count)
            labelStims.append(visual.TextStim(window,units = 'norm', text=labels[count], alignHoriz='center', alignVert='top', color=labelColor, height=0.05, pos=(pos,sliderLoc-0.05)))
            count += 1
    # Calculate the starting value for the slider at the middle, create the slider object and position it to the middle
    value = ( limits[1]-limits[0] )/2.0
    feedbackStim = visual.TextStim(window,units = 'norm', text=str(round(value,feedbackDigits)), height=0.04, color = feedbackColor, pos=(0,sliderLoc+0.05))

    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))

    mouse = event.Mouse(win=window)     # create the mouse object for responding to clicks

    def nearestLabel(x=None):
        """ Return the x position of the label nearest to the current x location - used for snap2labels """
        minDist = 99     # start with a number larger than the maximum distance between labels
        newPos = 0
        for label in labelStims:
            distance = abs(x-label.pos[0])
            if distance < minDist:
                minDist = distance
                newPos = label.pos[0]
        return newPos
    clickFirst = False
    # Ready for main look looking for clicks
    done = False
    startTime = clock.getTime()
    while (not done):
        drawAll()
        window.flip()
        while mouse.getPressed()[0] == 0: 
            drawAll()
            window.flip()# Wait for the mouse to be down
        x,y = mouse.getPos()
        if slider.contains(x,y) or sliderLine.contains(x,y):
            clickFirst = True
        if slider.contains(x,y) or (snap2mouse and sliderLine.contains(x,y)):
            while mouse.getPressed()[0] == 1:       # Loop for as long as the mouse stays down
                x,y = mouse.getPos()
                if snap2labels:
                    slider.setPos((nearestLabel(x),slider.pos[1]))
                else:
                    slider.setPos((min(max(x,-width),width),slider.pos[1]))
                if clickFirst == True or forceChoice == False:
                    next.draw()
                drawAll()
                if feedback == True:
                    vrange = limits[1]-limits[0]
                    value = pos2val(slider.pos[0])
                    if feedbackDigits == 0:
                        feedbackStim.setText(str(int(round(value))))
                    else:
                        feedbackStim.setText(str(round(value,feedbackDigits)))
                    feedbackStim.setPos((slider.pos[0],feedbackStim.pos[1]))
                    feedbackStim.draw()
                window.flip()
        elif next.contains(x,y):
            # If the subject clicked on the Next button, then darken it and track motion while the mouse is down.
            # If they move the mouse off the Next button before releasing it, lighten the button etc.
            # When they finally release the mouse button, consider the Next button clicked only if the mouse
            # is currently on it..
            clickTime = clock.getTime()
            next.setImage(pngPath+'darknext.png')
            while mouse.getPressed()[0] == 1:
                drawAll()
                window.flip()
                x,y = mouse.getPos()
                if next.contains(x,y):
                    next.setImage(pngPath+'darknext.png')
                else:
                    next.setImage(pngPath+'next.png')
            vrange = limits[1]-limits[0]
            if clickFirst == False:
                value = -999
            else:
                value = (((slider.pos[0] + (sliderLine.size[0]/2)) / sliderLine.size[0]) * vrange) + limits[0]
            x,y = mouse.getPos()
            if next.contains(x,y):
                rt = clickTime - startTime
                done = True
    window.flip()
    return round(value,feedbackDigits), rt

def scale(window,clock = None,
                drawList = [],
                width = 0.8,
                labels = ['left', 'right'],
                labelColor = 'white',
                nButtons = 5,
                numberButtons = False,
                forceChoice=True,
                scaleLoc = -0.6):
    """ Present a trial with a scale for response. The subject clicks on a scale button to highlight it,
    and then selects a value by clicking the Next button. Returns the
    number of the button highlighted when the Next button is clicked.
    
    Keyword arguments:
        window -- The parent window within which the slider is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        width -- The width of the slider relative to the window (default 0.8 or 80% of the window width)
        labels -- A list with the labels to be placed evenly spaced between the ends of the scale (default ['left', 'right'])
        labelColor -- Color of the label text (default 'white')
        nButtons -- the number of buttons in the scale
        numberButtons -- If True then the buttons will be numbered
        forceChoice -- If True, require the subject to select a scale button before displaying the Next button. (default True)
        scaleLoc -- vertical position of the scal in "norm" units. (default -0.6)
    """
    def drawAll():
        """ Draw all the objects that make up a slider trial """
        for item in drawList:
            item.draw()
        for index in range(len(scaleButtons)):
            scaleButtons[index].draw()
            if numberButtons:
                buttonNumbers[index].draw()
        for index in range(len(labelStims)):
            labelStims[index].draw()
        if nextVisible: next.draw()
     
     # create a clock if one is not provided
    if not clock:
        clock = core.Clock()
     
    # Build a list containing the labels. Calculate the positions for the labels so they are evenly spaced from end to end
    labelStims = []
    intervals = len(labels) - 1
    if intervals == 0:      # If only one label was given, position it in the middle
        labelStims.append(visual.TextStim(window,units = 'norm', text=labels[0], alignHoriz='center', alignVert='top', color=labelColor, height=0.05, pos=(0,scaleLoc - 0.1)))
    else: 
        spacing = (width*2)/intervals
        count = 0
        for label in labels:
            pos = -width + (spacing * count)
            labelStims.append(visual.TextStim(window,units = 'norm', text=labels[count], alignHoriz='center', alignVert='top', color=labelColor, height=0.05, pos=(pos,scaleLoc - 0.1)))
            count += 1

    # Build a list containing the scale buttons. Calculate the positions for the buttons so they are evenly spaced from end to end
    scaleButtons = []
    buttonNumbers = []
    intervals = nButtons - 1
    if intervals == 0:      # only one button, position it in the middle
        scaleButtons.append(visual.ImageStim(window, image = pngPath+'blank.png', mask = None, units = 'norm', pos=(0,scaleLoc)))
        buttonNumbers.append(visual.TextStim(window, units='norm', text='1', color='white', height=0.05, pos=(0,scaleLoc)))
    else: 
        spacing = (width*2)/intervals
        for count in range(nButtons):
            hpos = -width + (spacing * count)
            scaleButtons.append(visual.ImageStim(window, image = pngPath+'blank.png',  units = 'norm', pos=(hpos,scaleLoc)))
            buttonNumbers.append(visual.TextStim(window, units='norm', text=str(count+1), color='white', height=0.05, pos=(hpos,scaleLoc)))

    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))

    mouse = event.Mouse(win=window)     # create the mouse object for responding to clicks

    # Ready for main loop looking for clicks
    done = False
    selected = None
    if forceChoice:
        nextVisible = False
    else: 
        nextVisible = True

    startTime = clock.getTime()
    while (not done):
        drawAll()
        window.flip()
        
        while mouse.getPressed()[0] == 0:
            drawAll()
            window.flip()      # Wait for the mouse to be down
        x,y = mouse.getPos()
        for index in range(len(scaleButtons)):
            if scaleButtons[index].contains(x,y):
                if index == selected:
                    scaleButtons[selected].setImage(pngPath+'blank.png')
                    if forceChoice: nextVisible = False
                    selected = None
                else:
                    if selected != None: scaleButtons[selected].setImage(pngPath+'blank.png')
                    scaleButtons[index].setImage(pngPath+'darkblank.png')
                    selected = index
                    nextVisible = True
                # loop waiting for the mouse to be released
                while mouse.getPressed()[0] == 1:
                    drawAll()
                    window.flip()
        if nextVisible and next.contains(x,y):
            # If the subject clicked on the Next button, then darken it and track motion while the mouse is down.
            # If they move the mouse off the Next button before releasing it, lighten the button etc.
            # When they finally release the mouse button, consider the Next button clicked only if the mouse
            # is currently on it..
            clickTime = clock.getTime()
            next.setImage(pngPath+'darknext.png')
            while mouse.getPressed()[0] == 1:
                drawAll()
                window.flip()
                x,y = mouse.getPos()
                if next.contains(x,y):
                    next.setImage(pngPath+'darknext.png')
                else:
                    next.setImage(pngPath+'next.png')
            x,y = mouse.getPos()
            if next.contains(x,y):
                rt = clickTime - startTime
                done = True
    window.flip()
    return selected, rt

def bars(window,clock = None,
                drawList = [],
                width = 0.8,
                height = 0.8,
                labels = None,
                labelColors = None,
                yLabels = None,
                yLabelColors = None,
                barColors = None,
                nBars = 5,
                limits = [0.0,100.0],
                defaultHeight = None,
                drawAxes = True,
                forceChoice=True):
    """ Present a trial with a bar chart for response. The subject clicks and drags the bars to the desired height,
    and then selects these values by clicking the Next button. Returns the
    heights of the bars when the Next button is clicked.
    
    Keyword arguments:
        window -- The parent window within which the barchart is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the barchart
        width -- The width of the barchart relative to the window (default 0.8 or 80% of the window width)
        height -- the height of the barchart in window coordinates ( default: 0.8)
        labels -- A list with the labels to be placed evenly spaced between the ends of the barchart (default None)
        labelColors -- A list of colors for the labels (default: black if background is white, white otherwise)
        yLabels -- a list of labes to be evenly paced to the left of the Y axis
        yLabelColors -- A list of colors for the Y labels (default: black if background is white, white otherwise)
        barColors -- A list of colors for the bars (default: white if background is grey, grey otherwise)
        nBars -- the number of bars in the chart
        limits -- a two item list with the min and max values for the bar chart (default: [0.0,100.0])
        defaultHeight -- the default bar height in the units of limits above (default: halfway)
                                  can also be a list with heights for each bar (must be nBars long)
        drawAxes -- if True, draw X and Y axes for the bar chart (default: True)
        forceChoice -- If True, require the subject to move a bar before displaying the Next button. (default True)
    """
    def drawAll():
        """ Draw all the objects that make up a slider trial """
        for item in drawList:
            item.draw()
        for index in range(len(bars)):
            bars[index].draw()
        for index in range(len(labelStims)):
            labelStims[index].draw()
        for index in range(len(yLabelStims)):
            yLabelStims[index].draw()
        if drawAxes: axes.draw()
        if nextVisible: next.draw()
     
    def barClicked(x = None, y = None, bar = None):
        """ Check to see if the click location (x,y) is within the bounds of object
        """
        left = bar.pos[0] + bar.vertices[0][0]
        right = bar.pos[0] + bar.vertices[2][0]
        top = bar.pos[1] + bar.vertices[1][1]
        bottom = bar.pos[1] + bar.vertices[0][1]
    
        if x < right and x > left and y < top and y > bottom:
            return True
        else:
            return False
            
     # create a clock if one is not provided
    if not clock:
        clock = core.Clock()
     
    bars = []
    barNumbers = []
    base = -.65
    maxPos = base + height
    maxHeight = maxPos - base
    barWidth = (width * 2.0) / nBars
    barGap = barWidth/10.0
    if not defaultHeight:
        defaultHeight = (limits[1]-limits[0])/2.0 + limits[0]

    # Build a list containing the labels. Calculate the positions for the labels so they are evenly spaced from end to end
    labelStims = []
    if labels:
        intervals = len(labels) - 1
        if not labelColors:
            if window.color == 'white': labelColor = 'black'
            else: labelColor = 'white'
            labelColors = []
            for label in labels:
                labelColors.append(labelColor)
        if intervals == 0:      # If only one label was given, position it in the middle
            labelStims.append(visual.TextStim(window,units = 'norm', text=labels[0], alignHoriz='center', alignVert='top', color=labelColors[0], height=0.05, pos=(0,-0.7)))
        else: 
            spacing = ((width*2)-barWidth)/intervals
            count = 0
            for label in labels:
                pos = -width + (barWidth/2.0) + (spacing * count)
                labelStims.append(visual.TextStim(window,units = 'norm', text=labels[count], alignHoriz='center', alignVert='top', color=labelColors[count], height=0.05, pos=(pos,-0.7)))
                count += 1

    # Build a list containing the Y labels. Calculate the positions for the labels so they are evenly spaced from bottom to top
    yLabelStims = []
    if yLabels:
        if not yLabelColors:
            if window.color == 'white': labelColor = 'black'
            else: labelColor = 'white'
            yLabelColors = []
            for label in yLabels:
                yLabelColors.append(labelColor)
        intervals = len(yLabels) - 1
        if intervals == 0:      # If only one label was given, position it in the middle
            yLabelStims.append(visual.TextStim(window,units = 'norm', text=yLabels[0], color=yLabelColors[0], height=0.05, alignHoriz='right',pos=(-width-.01,base+(maxPos-base)/2.0)))
        else: 
            spacing = (maxPos-base)/intervals
            count = 0
            for label in yLabels:
                pos = base + (spacing * count)
                yLabelStims.append(visual.TextStim(window,units = 'norm', text=yLabels[count], color=yLabelColors[count], height=0.05, alignHoriz='right', pos=(-width-.01,pos)))
                count += 1

    # Build a list containing the bars. Calculate the positions for the bars so they are evenly spaced within the width specified

    if not barColors:
        if window.color == 'lightgrey': barColor = 'white'
        else: barColor = 'lightgrey'
        barColors = []
        for count in range(nBars):
            barColors.append(barColor)
    for count in range(nBars):
        barPos = -1 + (1.0-width) + (count * barWidth) + barWidth/2.0
        left = -(barWidth/2.0)+barGap
        right = (barWidth/2.0)-barGap
        if type(defaultHeight).__name__ != 'list':
            top = ((defaultHeight-limits[0])/(limits[1]-limits[0])) * height
        else:
            if count+1 > len(defaultHeight):
                print 'Warning: defaultHeight list is too short, using .5 for bar %i' % (count+1)
                top = .5 * height
            else:
                top = ((defaultHeight[count]-limits[0])/limits[1]-limits[0]) * height
        barVertices = [ [left,-.01], [left,top],[right,top], [right,-.01] ]
        bars.append( visual.ShapeStim(window, 
                 lineColor='black',
                 lineWidth=2.0, #in pixels
                 fillColor=barColors[count], #beware, with convex shapes fill colors don't work
                 vertices=barVertices,#choose something from the above or make your own
                 closeShape=True,#do you want the final vertex to complete a loop with 1st?
                 pos= [barPos,base], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=0.9,
                 autoLog=False))#this stim changes too much for autologging to be useful

    # create axes
    if drawAxes:
        if window.color == 'black': axisColor = 'white'
        else: axisColor = 'black'
        axes = visual.ShapeStim(window, 
                 lineColor=axisColor,
                 lineWidth=2.0, #in pixels
                 fillColor=None, #beware, with convex shapes fill colors don't work
                 vertices=[[width,base-.01],[-width,base-.01],[-width,maxPos]],#choose something from the above or make your own
                 closeShape=False,#do you want the final vertex to complete a loop with 1st?
                 pos= [0,0], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=1.0,
                 autoLog=False)#this stim changes too much for autologging to be useful
                 
    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))

    mouse = event.Mouse(win=window)     # create the mouse object for responding to clicks

    # Ready for main loop looking for clicks
    done = False
    if forceChoice:
        nextVisible = False
    else: 
        nextVisible = True

    startTime = clock.getTime()
    while (not done):
        drawAll()
        window.flip()
        
        while mouse.getPressed()[0] == 0: 
            drawAll()
            window.flip()      # Wait for the mouse to be down
        x,y = mouse.getPos()
        for index in range(len(bars)):
            
            if barClicked(x,y,bars[index]):
                # loop waiting for the mouse to be released
                nextVisible = True
                vertices = bars[index].vertices
                top = vertices[1][1]
                while mouse.getPressed()[0] == 1:
                    newX,newY = mouse.getPos()
                    deltaY = newY - y
                    setting = max(0.0,min(maxPos-base, top+deltaY))
                    vertices[1][1] = setting
                    vertices[2][1] = setting
                    bars[index].setVertices(vertices)
                    drawAll()
                    window.flip()

        if nextVisible and next.contains(x,y):
            # If the subject clicked on the Next button, then darken it and track motion while the mouse is down.
            # If they move the mouse off the Next button before releasing it, lighten the button etc.
            # When they finally release the mouse button, consider the Next button clicked only if the mouse
            # is currently on it..
            clickTime = clock.getTime()
            next.setImage(pngPath+'darknext.png')
            while mouse.getPressed()[0] == 1:
                drawAll()
                window.flip()
                x,y = mouse.getPos()
                if next.contains(x,y):
                    next.setImage(pngPath+'darknext.png')
                else:
                    next.setImage(pngPath+'next.png')
            x,y = mouse.getPos()
            if next.contains(x,y):
                rt = clickTime - startTime
                done = True
    settings = []
    for bar in bars:
        settings.append( (bar.vertices[1][1]/height) * (limits[1]-limits[0]) + limits[0] )
    window.flip()
    return settings,rt

def choice(window,clock = None,
                    drawList=[],
                    vPos = 0.0,
                    hPos = -0.2,
                    labels=['a','b','c','d','e'],
                    labelColor='white',
                    labelSize=0.1,
                    forceChoice=True):
    """ Present a trial with a set of radio buttons. Only one radio button my be selected.
    Return the number of the selected button or None if no buttons are selected when the Next button is selected.
    
    Keyword arguments:
        window -- The parent window within which the slider is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        vPos -- The vertical position of the first item on the list of radio buttons. The buttons will
                    be spaced evenly between this location ant the Next button at the bottom of the window. (default 0.0)
        hPos -- The horizontal position of the left edge of the radio button items (default -0.2)
        labels -- A list with the radio button labels to be placed evenly spaced between vPos and the Next button (default ['a','b','c','d','e'])
        labelColor -- Color of the label text (default 'white')
        labelSize -- Size of the text of the labels (default 0.1)
        forceChoice -- If True, require the subject to select a radio button before displaying the Next button. (default True)
    """
    def drawAll():
        """ Draw all objects """
        for item in drawList: item.draw()
        for label in labelStims: label.draw()
        for rb in rbStims: rb.draw()
        if nextVisible: next.draw()
     
     # create a clock if one is not provided
    if not clock:
        clock = core.Clock()

    aspectRatio = (float(window.size[1])/float(window.size[0]))       # This is needed when scaling the radio buttons so they stay round
    vInc = abs(-.9 - vPos)/(len(labels)+1)      # spacing to use between labels
    
    # Build the lists or label and radio button stimuli
    labelStims = []
    rbStims = []
    for index in range(len(labels)):
        v = vPos - vInc * index
        labelStims.append(visual.TextStim(window,units = 'norm', text=labels[index], alignHoriz = 'left', height=labelSize, color = labelColor, pos=(hPos,v)))
        rbSize=labelSize*.5     # The radio buttons look too big if not scaled down relative to the labels
        rbStims.append(visual.ImageStim(window,image=pngPath+'rb.png', size=(rbSize*aspectRatio,rbSize),units = 'norm', pos=(hPos-rbSize,v-labelSize*.05)))

    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))


    mouse = event.Mouse(win=window)
    done = False
    selected = None
    if forceChoice:
        nextVisible = False
    else: 
        nextVisible = True
    # Main loop waiting for clicks
    startTime = clock.getTime()
    while (not done):
        drawAll()
        window.flip()
        
        while mouse.getPressed()[0] == 0: 
            drawAll()
            window.flip()      # Wait for click
        x,y = mouse.getPos()
        for index in range(len(rbStims)):
            if rbClicked(x,y,rbStims[index],extendRight=True):
                if index == selected:
                    rbStims[selected].setImage(pngPath+'rb.png')
                    if forceChoice: nextVisible = False
                    selected = None
                else:
                    if selected != None: rbStims[selected].setImage(pngPath+'rb.png')
                    rbStims[index].setImage(pngPath+'rbc.png')
                    selected = index
                    nextVisible = True
                # loop waiting for the mouse to be released
                while mouse.getPressed()[0] == 1:
                    drawAll()
                    window.flip()
        # If the subject clicked on the Next button, then darken it and track motion while the mouse is down.
        # If they move the mouse off the Next button before releasing it, lighten the button etc.
        # When they finally release the mouse button, consider the Next button clicked only if the mouse
        # is currently on it..
        if nextVisible and next.contains(x,y):
            clickTime = clock.getTime()
            next.setImage(pngPath+'darknext.png')
            while mouse.getPressed()[0] == 1:
                drawAll()
                window.flip()
                x,y = mouse.getPos()
                if next.contains(x,y):
                    next.setImage(pngPath+'darknext.png')
                else:
                    next.setImage(pngPath+'next.png')
            x,y = mouse.getPos()
            if next.contains(x,y):
                rt = clickTime - startTime
                done = True
    window.flip()
    return selected, rt

def multiChoice(window,clock = None,
                    drawList=[],
                    vPos = 0.0, hPos = -0.2,
                    labels=['a','b','c','d','e'],
                    labelColor='white',
                    labelSize=0.1,
                    forceChoice = True):
    """ Present a trial with a set of check boxes. Any number of check boxes may be selected.
    Return a list of the numbers of the selected boxes or an empty list if no boxes are selected when the Next button is selected.
    
    Keyword arguments:
        window -- The parent window within which the slider is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        vPos -- The vertical position of the first item on the list of check boxes. The boxes will
                    be spaced evenly between this location ant the Next button at the bottom of the window. (default 0.0)
        hPos -- The horizontal position of the left edge of the check box items (default -0.2)
        labels -- A list with the check box labels to be placed evenly spaced between vPos and the Next button (default ['a','b','c','d','e'])
        labelColor -- Color of the label text (default 'white')
        labelSize -- Size of the text of the labels (default 0.1)
        forceChoice -- If True, require the subject to select at least one box before displaying the Next button. (default True)
    """

    def drawAll():
        for item in drawList: item.draw()
        for label in labelStims: label.draw()
        for rb in rbStims: rb.draw()
        if nextVisible: next.draw()
    if forceChoice:
        nextVisible = False
    else:
        nextVisible = True
     
     # create a clock if one is not provided
    if not clock:
        clock = core.Clock()

    aspectRatio = (float(window.size[1])/float(window.size[0]))
    vInc = abs(-.9 - vPos)/(len(labels)+1)
    labelStims = []
    rbStims = []
    
    for index in range(len(labels)):
        v = vPos - vInc * index
        labelStims.append(visual.TextStim(window,units = 'norm', text=labels[index], alignHoriz = 'left', height=labelSize, color = labelColor, pos=(hPos,v)))
        rbSize=labelSize*.5
        rbStims.append(visual.ImageStim(window,image=pngPath+'box.png', size=(rbSize*aspectRatio,rbSize),units = 'norm', pos=(hPos-rbSize,v-labelSize*.05)))
    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))
     
    mouse = event.Mouse(win=window)
    done = False
    selected = []
    startTime = clock.getTime()
    while (not done):
        drawAll()
        window.flip()
        
        while mouse.getPressed()[0] == 0:
            drawAll()
            window.flip()      # Wait for a click
        x,y = mouse.getPos()
        for index in range(len(rbStims)):
            if rbClicked(x,y,rbStims[index],extendRight=True):
                if nextVisible == False: nextVisible = True
                if index not in selected:
                    rbStims[index].setImage(pngPath+'boxc.png')
                    while mouse.getPressed()[0] == 1:
                        drawAll()
                        window.flip()
                    selected.append(index)
                else:
                    rbStims[index].setImage(pngPath+'box.png')
                    while mouse.getPressed()[0] == 1:
                        drawAll()
                        window.flip()
                    selected.remove(index)
                    if len(selected) == 0: nextVisible = False
        # If the subject clicked on the Next button, then darken it and track motion while the mouse is down.
        # If they move the mouse off the Next button before releasing it, lighten the button etc.
        # When they finally release the mouse button, consider the Next button clicked only if the mouse
        # is currently on it..
        if nextVisible and next.contains(x,y):
            clickTime = clock.getTime()
            next.setImage(pngPath+'darknext.png')
            while mouse.getPressed()[0] == 1:
                drawAll()
                window.flip()
                x,y = mouse.getPos()
                if next.contains(x,y):
                    next.setImage(pngPath+'darknext.png')
                else:
                    next.setImage(pngPath+'next.png')
            x,y = mouse.getPos()
            if next.contains(x,y): 
                rt = clickTime - startTime
                done = True
    window.flip()
    return selected, rt


def textInput(window, clock=None,
                      drawList=[],
                      prompt='Enter your response:',
                      promptHeight=0.065,
                      promptOffset = 0.1,
                      promptColor='white',
                      boxTop=0.0):
    boxWidth=0.8
    promptPos= (-boxWidth, boxTop+promptOffset)
    if not clock:
        clock=core.Clock()
    prompt = visual.TextStim(window,text=prompt,font='Arial',height=promptHeight,alignHoriz='left',color=promptColor, pos=promptPos,alignVert='top', wrapWidth=boxWidth*2)
    writeBox=visual.ShapeStim(window, lineWidth=2.0, lineColor='black', fillColor='white', vertices=((-boxWidth,boxTop), (boxWidth,boxTop), (boxWidth,-0.75), (-boxWidth,-0.75) ), closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0)
    global message
    message = ''
    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))
    textfield = visual.TextStim(window,text=message+'_',font='Arial',height=.05,alignVert='top', alignHoriz='left',color='black',pos=(-boxWidth+0.05,boxTop-0.05), wrapWidth=boxWidth*2-0.1)

    """ Present a trial with text input box. 
    Returns the entered text and the time when the next button is pressed. 
    
    Keyword arguments:
        window -- The parent window within which the text input box is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        prompt -- Text that appears as instructions above the text input box. (default = "Enter your response:")
        promptHeight -- The size of the prompt text (default = 0.065)
        promptOffset -- The distance that the prompt appears from the text input box (default = 0.1)
        promptColor -- Color of the prompt text (default = 'white')
        boxTop -- Position of the top of the text input box in normal window units (-1.0 to 1.0) (default = 0.0, center of the screen)
        
        
        
    """
    def drawAll():
        for item in drawList:
            item.draw()
        writeBox.draw()
        prompt.draw()
        textfield.draw()
        next.draw()

    def myTextHandler(text):
        global message
        if text == chr(13): text = '\n'
        message += text
        textfield.setText(message+'_')

    def myTextMotionHandler(motion):
        global message
        if motion == pyglet.window.key.MOTION_BACKSPACE:
            message = message[0:-1]
        textfield.setText(message+'_')
    

    mouse = event.Mouse(win=window)
    done = False
    startTime = clock.getTime()
    
    orig_on_text = window.winHandle.on_text
    window.winHandle.on_text = myTextHandler
    window.winHandle.on_text_motion = myTextMotionHandler
    while (not done):
        drawAll()
        window.flip()
        if mouse.getPressed()[0] == 1:
            x,y = mouse.getPos()
            if next.contains(x,y):
                clickTime = clock.getTime()
                next.setImage(pngPath+'darknext.png')
                while mouse.getPressed()[0] == 1:
                    drawAll()
                    window.flip()
                    x,y = mouse.getPos()
                    if next.contains(x,y):
                        next.setImage(pngPath+'darknext.png')
                    else:
                        next.setImage(pngPath+'next.png')
                x,y = mouse.getPos()
                if next.contains(x,y): 
                    rt = clickTime - startTime
                    done = True 
    window.winHandle.on_text = orig_on_text
    del window.winHandle.on_text_motion
    window.flip()
    return message,rt

class Field():
    def __init__(self, window, fieldtype='string', maxChars=12, size=0.1, text=None, label=None, labelColor='black', pos=[0,0]):
        width = (size*0.6) * maxChars
        self.charsTyped = False
        self.text = text
        if self.text is not None:
            self.text = str(self.text)
        self.fieldtype = fieldtype
        self.maxChars = maxChars
        self.tstim = visual.TextStim(window,text=text,font='Arial',height=size,alignHoriz='left',color='black', pos=(pos[0]+.02,pos[1]))
#        self.writeBox=visual.ShapeStim(window, lineWidth=2.0, lineColor='black', fillColor='white', vertices=( (pos[0]+.01,pos[1]-size/2-.01), (pos[0]+.01+width,pos[1]-size/2-.01), (pos[0]+.01+width,pos[1]+size/2), (pos[0]+.01,pos[1]+size/2) ), closeShape=True)
        self.writeBox=visual.Rect(window, lineWidth=2.0, height=size+0.01, width = width,lineColor='black', fillColor='white', pos = (pos[0]+0.01+(width/2), pos[1]-0.01), closeShape=True)
        self.label = label
        if self.label != None: self.labelStim =  visual.TextStim(window, text=self.label, alignHoriz = 'right', height=.1, color = labelColor, pos=pos)
        if fieldtype != 'string':
            if fieldtype == 'letters':
                self.checkInput = re.compile('[a-z]|[A-Z]')
            elif fieldtype == 'int':
                if self.text != None: test = int(self.text)
                self.checkInput = re.compile('[0-9]')
            elif fieldtype == 'float':
                if self.text != None: test = float(self.text)
                self.checkInput = re.compile('[0-9.]')
    
    def textHandler(self, text):
        if not self.charsTyped:
            self.text = ''
            self.charsTyped = True
        if len(self.text) < self.maxChars:
            if self.fieldtype != 'string':
                if not self.checkInput.match(text):
                    text = ''
            if text == chr(13):
                text = ''
            if self.fieldtype == 'float' and text == '.' and '.' in self.text:
                text = ''
            self.text += text
            self.tstim.setText(self.text)
            
    def textMotionHandler(self, motion):
        if not self.charsTyped:
            self.text = ''
            self.charsTyped = True
        if motion == pyglet.window.key.MOTION_BACKSPACE:
            self.text = self.text[0:-1]
        self.tstim.setText(self.text)
        
    def draw(self):
        self.writeBox.draw()
        self.tstim.draw()
        if self.label != None: self.labelStim.draw()
        
    def getResponse(self):
        response = self.text
#        if self.fieldtype == 'int' and len(self.text) > 0: response = int(self.text)
#        elif self.fieldtype == 'float' and len(self.text) > 0: response = float(self.text)
        return response

def form(window, clock=None,
                      drawList=[],
                      fields = [ ['label1', 'black', 'L1', 12, 'string'], ['label2', 'black', '3.2', 12, 'string'] ],
                      size=.1,
                      pos = [0,0],
                      timeout = None):
    """ Present a trial with multiple text fields. 
    Returns the entered text and the time when the next button is pressed. 
    
    Keyword arguments:
        window -- The parent window within which the text input box is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        fields -- a list of field descriptor lists. Each field descriptor list must have the 5 following elements:
              label - the text label to appear to the left of the field
              labelColor - color of the text label
              text - Initial text that appears in the box - will be replaced by typed characters. (default = empty)
              maxChars - Maximum nuber of characters (default = 12)
              fieldtype - Limit the entered data by limiting input to valid characters - 'string', 'letters', 'int', or 'float' (default: string (any characters))
        size -- The size of the text (default = 0.1)
        pos -- Position of the left edge of the first field box (default = [0,0])
        timeout -- number of seconds after which to time out (default = None)
        
    """
    if not clock:
        clock=core.Clock()
    formFields = []
    x, y = pos
    for field in fields:
        label, labelColor, text, max, fieldtype = field
        fieldpos = [x, y]
        y -= (size + 0.03)
        formFields.append(Field(window, label=label, maxChars=max, pos=fieldpos, fieldtype=fieldtype, text=text))
    activeField = formFields[0]
    next = visual.ImageStim(window,image=pngPath+'next.png', units = 'norm', pos=(0,-0.9))

    def drawAll():
        for item in drawList:
            item.draw()
        for field in formFields:
            activeField.writeBox.lineWidth=4
            field.draw()
            activeField.writeBox.lineWidth=1
        next.draw()
        
    def myTextHandler(text):
        activeField.textHandler(text)
    def myTextMotionHandler(motion):
        activeField.textMotionHandler(motion)
    

    mouse = event.Mouse(win=window)
    done = False
    if timeout != None:
        tclock = core.Clock()
        tclock.reset()
    startTime = clock.getTime()
    
    orig_on_text = window.winHandle.on_text
    window.winHandle.on_text =myTextHandler
    window.winHandle.on_text_motion = myTextMotionHandler
    while (not done):
        drawAll()
        window.flip()
        if timeout != None and tclock.getTime() > timeout:
            rt= -99
            done = True
        if mouse.getPressed()[0] == 1:
            x,y = mouse.getPos()
            for field in formFields:
                if field.writeBox.contains(x,y):
                    activeField = field
            if next.contains(x,y):
                clickTime = clock.getTime()
                next.setImage(pngPath+'darknext.png')
                while mouse.getPressed()[0] == 1:
                    drawAll()
                    window.flip()
                    x,y = mouse.getPos()
                    if next.contains(x,y):
                        next.setImage(pngPath+'darknext.png')
                    else:
                        next.setImage(pngPath+'next.png')
                x,y = mouse.getPos()
                if next.contains(x,y): 
                    rt = clickTime - startTime
                    done = True 
    window.winHandle.on_text = orig_on_text
    del window.winHandle.on_text_motion
    window.flip()
    responses = []
    for field in formFields:
        responses.append(field.getResponse())
    return responses,rt

def textField(window, clock=None,
                      label = 'your label',
                      labelColor = 'black',
                      drawList=[],
                      text=None,
                      maxChars=12,
                      size=.1, pos=[0,0],
                      fieldtype='string',
                      timeout = None):
    """ Present a trial with text field box (one line - limited length). 
    Returns the entered text and the time when the next button is pressed. 
    
    Keyword arguments:
        window -- The parent window within which the text input box is drawn
        clock -- If provided, the psychopy clock object will be used for timing. If not, one will be created.
        drawList -- A list of objects that should be drawn along with the slider
        label -- text label to be placed to the left of the field
        labelColor -- color of the text label
        text -- Initial text that appears in the box - will be replaced by typed characters. (default = empty)
        maxChars -- Maximum nuber of characters (default = 8)
        size -- The size of the text (default = 0.1)
        pos -- Position of the left edge of the box - centered vertically (default = [0,0])
        fieldtype -- Limit the entered data by limiting input to valid characters - 'string', 'letters', 'int', or 'float' (default: string (any characters))
        timeout -- number of seconds after which to time out default = None)
    """
    return form(window=window, drawList=drawList, fields = [ [label, labelColor, text, maxChars, fieldtype] ], size = size, pos = pos, timeout = timeout )
    