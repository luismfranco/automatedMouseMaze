"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from psychopy import visual
import pandas as pd


"""
Drifting Gratings

"""

class driftingGratings:
    
    def __init__(self, stimulusScreen, screenSize):
    
        # Create stimulus window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen, units = "deg",
                                            size = screenSize, fullscr = True, color = (0.5, 0.5, 0.5))
        
        # Orientation
        self.leftTargetOrientation = 90
        self.rightTargetOrientation = 0
        
        # Stimulus
        self.showVisualStimulus = False
        
        # Stimulus settings
        self.stimulusMask = None                                # "raisedCos", None
        self.stimulusSize = self.stimulusWindow.size.tolist()   # self.stimulusWindow.size.tolist(), 20 (only relevant when mask is not None)
        self.targetPosition = [0, 0]                            # [0, 0] <-- centered in the middle of the screen
        self.spatialFrequency = 0.1                             # 0.1
        self.xPositionOffset = 0                                # 0, 7 (only relevant when mask is not None)
        self.phaseOffset = 0.025                                # 0.025, move phase by 0.025 of a cycle
        
    def retrieveStimulusParameters(self):
        
        # Table for stimulus settings
        stimulusParameters = {
                          "leftTargetOrientation": str(self.leftTargetOrientation),
                          "rightTargetOrientation": str(self.rightTargetOrientation),
                          "stimulusMask": str(self.stimulusMask),
                          "stimulusSize": str(self.stimulusSize),
                          "targetPosition": str(list(self.targetPosition)),
                          "spatialFrequency": str(self.spatialFrequency),
                          "xPositionOffset": str(self.xPositionOffset),
                          "phaseOffset": str(self.phaseOffset),
                                                                               }
        stimulusParameters = pd.DataFrame.from_dict(stimulusParameters, orient = 'index')
        
        return stimulusParameters
    
    def initializeStimulus(self, **kwargs):
        
        # Initialize stimulus
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.targetOrientation = self.leftTargetOrientation
        elif self.targetLocation == 1:
            self.targetOrientation = self.rightTargetOrientation
        self.grating = visual.GratingStim(win = self.stimulusWindow, mask = self.stimulusMask, size = self.stimulusSize,
                                          pos = self.targetPosition, sf = self.spatialFrequency, ori = self.targetOrientation)
        
    def startStimulus(self, **kwargs):
        
        # Stimulus offset
        if self.targetLocation == 0:
            self.grating.setPos([-1 * self.xPositionOffset, 0])
        elif self.targetLocation == 1:
            self.grating.setPos([     self.xPositionOffset, 0])
            
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.grating.setOpacity(1)
        self.stimulusWindow.update()
        
    # Draw and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            if self.targetLocation == 0:
                self.grating.setPhase(self.phaseOffset, '-')
            elif self.targetLocation == 1:
                self.grating.setPhase(self.phaseOffset, '+')
            self.grating.draw()
            self.stimulusWindow.update()
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.grating.setOpacity(0)
        self.stimulusWindow.update()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()
        
        
"""
Main Block

"""

if __name__ == "__main__":
    driftingGratings = driftingGratings.__init__()