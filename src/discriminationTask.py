"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from psychopy import visual
import pandas as pd


"""
Discrimination Task

"""

class filledCircles:
    
    def __init__(self, stimulusScreen, screenSize):
    
        # Create stimulus window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen, units = 'deg',
                                            size = screenSize, fullscr = True, color = (0, 0, 0))
        
        # Orientation
        self.leftTargetColor = (-1, -1, -1)
        self.rightTargetColor = (-1, -1, -1)
        self.leftDistractorColor = (1, 1, 1)
        self.rightDistractorColor = (1, 1, 1)
        
        # Stimulus
        self.showVisualStimulus = False
        
        # Stimulus settings
        self.radius = 1                                         # radius of the circle
        self.stimulusSize = 5                                   # scaling factor of the circle
        self.targetPosition = [0, 0]                            # [0, 0] <-- centered in the middle of the screen
        self.xPositionOffset = 10                               # 10
        self.yPositionOffset = -4                               # -4
        
    def retrieveStimulusParameters(self):
        
        # Table for stimulus settings
        stimulusParameters = {
                          "leftTargetColor": str(self.leftTargetColor),
                          "rightTargetColor": str(self.rightTargetColor),
                          "leftDistractorColor": str(self.leftDistractorColor),
                          "rightDistractorColor": str(self.rightDistractorColor),
                          "stimulusRadius": str(self.radius),
                          "stimulusSize": str(self.stimulusSize),
                          "targetPosition": str(list(self.targetPosition)),
                          "xPositionOffset": str(self.xPositionOffset),
                          "yPositionOffset": str(self.yPositionOffset),
                                                                               }
        stimulusParameters = pd.DataFrame.from_dict(stimulusParameters, orient = 'index')
        
        return stimulusParameters
    
    def initializeStimulus(self, **kwargs):
        
        # Initialize stimulus
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.targetColor = self.leftTargetColor
            self.distractorColor = self.rightDistractorColor
        elif self.targetLocation == 1:
            self.targetColor = self.rightTargetColor
            self.distractorColor = self.leftDistractorColor
        
        self.targetObject = visual.Circle(win = self.stimulusWindow, size = self.stimulusSize, radius = self.radius,
                                          pos = self.targetPosition, color = self.targetColor, colorSpace = 'rgb')
        self.distractorObject = visual.Circle(win = self.stimulusWindow, size = self.stimulusSize, radius = self.radius,
                                              pos = self.targetPosition, color = self.distractorColor, colorSpace = 'rgb')
        
    def startStimulus(self, **kwargs):
        
        # Stimulus offset
        if self.targetLocation == 0:
            self.targetObject.setPos([    -1 * self.xPositionOffset, self.yPositionOffset])
            self.distractorObject.setPos([     self.xPositionOffset, self.yPositionOffset])
        elif self.targetLocation == 1:
            self.targetObject.setPos([         self.xPositionOffset, self.yPositionOffset])
            self.distractorObject.setPos([-1 * self.xPositionOffset, self.yPositionOffset])
            
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.targetObject.setOpacity(1)
        self.distractorObject.setOpacity(1)
        self.targetObject.draw()
        self.distractorObject.draw()
        self.stimulusWindow.flip()
        
    # Draw and update the stimulus
    def updateStimulus(self):
        
        # Circles are static. No need to update them.
        ...
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.targetObject.setOpacity(0)
        self.distractorObject.setOpacity(0)
        self.targetObject.draw()
        self.distractorObject.draw()
        self.stimulusWindow.flip()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()


class driftingGratings:
    
    def __init__(self, stimulusScreen, screenSize):
    
        # Create stimulus window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen, units = "deg",
                                            size = screenSize, fullscr = True, color = (0.5, 0.5, 0.5))
        
        # Orientation
        self.leftTargetOrientation = 0
        self.rightDistractorOrientation = 90
        self.rightTargetOrientation = 0
        self.leftDistractorOrientation = 90
        
        # Stimulus
        self.showVisualStimulus = False
        
        # Stimulus settings
        self.stimulusMask = "raisedCos"                         # "raisedCos", None
        self.stimulusSize = 12.5                                # self.stimulusWindow.size.tolist(), 20 (only relevant when mask is not None)
        self.targetPosition = [0, 0]                            # [0, 0] <-- centered in the middle of the screen
        self.spatialFrequency = 0.1                             # 0.1
        self.xPositionOffset = 8                                # 0, 7 (only relevant when mask is not None)
        self.yPositionOffset = -2                               # 0, -2 (only relevant when mask is not None)
        self.phaseOffset = 0.025                                # 0.025, move phase by 0.025 of a cycle
        
    def retrieveStimulusParameters(self):
        
        # Table for stimulus settings
        stimulusParameters = {
                          "leftTargetOrientation": str(self.leftTargetOrientation),
                          "rightTargetOrientation": str(self.rightTargetOrientation),
                          "rightDistractorOrientation": str(self.rightDistractorOrientation),
                          "leftDistractorOrientation": str(self.leftDistractorOrientation),
                          "stimulusMask": str(self.stimulusMask),
                          "stimulusSize": str(self.stimulusSize),
                          "targetPosition": str(list(self.targetPosition)),
                          "spatialFrequency": str(self.spatialFrequency),
                          "xPositionOffset": str(self.xPositionOffset),
                          "yPositionOffset": str(self.yPositionOffset),
                          "phaseOffset": str(self.phaseOffset),
                                                                               }
        stimulusParameters = pd.DataFrame.from_dict(stimulusParameters, orient = 'index')
        
        return stimulusParameters
    
    def initializeStimulus(self, **kwargs):
        
        # Initialize stimulus
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.targetOrientation = self.leftTargetOrientation
            self.distractorOrientation = self.rightDistractorOrientation
        elif self.targetLocation == 1:
            self.targetOrientation = self.rightTargetOrientation
            self.distractorOrientation = self.leftDistractorOrientation
        self.targetObject = visual.GratingStim(win = self.stimulusWindow, mask = self.stimulusMask, size = self.stimulusSize,
                                          pos = self.targetPosition, sf = self.spatialFrequency, ori = self.targetOrientation)
        self.distractorObject = visual.GratingStim(win = self.stimulusWindow, mask = self.stimulusMask, size = self.stimulusSize,
                                                   pos = self.targetPosition, sf = self.spatialFrequency, ori = self.distractorOrientation)
        
    def startStimulus(self, **kwargs):
        
        # Stimulus offset
        if self.targetLocation == 0:
            self.targetObject.setPos(    [-1 * self.xPositionOffset, self.yPositionOffset])
            self.distractorObject.setPos([     self.xPositionOffset, self.yPositionOffset])
        elif self.targetLocation == 1:
            self.targetObject.setPos(    [     self.xPositionOffset, self.yPositionOffset])
            self.distractorObject.setPos([-1 * self.xPositionOffset, self.yPositionOffset])
            
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.targetObject.setOpacity(1)
        self.distractorObject.setOpacity(1)
        self.stimulusWindow.update()
        
    # Draw and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            if self.targetLocation == 0:
                self.targetObject.setPhase(self.phaseOffset, '+')
                self.distractorObject.setPhase(self.phaseOffset, '-')
            elif self.targetLocation == 1:
                self.targetObject.setPhase(self.phaseOffset, '+')
                self.distractorObject.setPhase(self.phaseOffset, '-')
            self.targetObject.draw()
            self.distractorObject.draw()
            self.stimulusWindow.update()
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.targetObject.setOpacity(0)
        self.distractorObject.setOpacity(0)
        self.stimulusWindow.update()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()
        
        
"""
Main Block

"""

if __name__ == "__main__":
    filledCircles = filledCircles.__init__()
    driftingGratings = driftingGratings.__init__()