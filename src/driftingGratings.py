"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from psychopy import visual

# changes made by cf - 12/16/24: self.leftTarget = 180 instead of 90, added self.gratingsetPos (7,0), changed self.grating.setPhase(0.025, '-') to 0.025,+
"""
Drifting Gratings

"""

class driftingGratings:
    
    def __init__(self, stimulusScreen, screenSize):
    
        # Create stimulus window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen, units = "deg",
                                            size = screenSize, fullscr = True, color = (1.0, 1.0, 1.0))
        
        # Orientation
        self.leftTarget = 90
        self.rightTarget = 0
        
        # Stimulus
        self.showVisualStimulus = False
        
    def initializeStimulus(self, **kwargs):
        
        # Initialize stimulus
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.target = self.leftTarget
        elif self.targetLocation == 1:
            self.target = self.rightTarget
        self.grating = visual.GratingStim(win = self.stimulusWindow, mask = "raisedCos", size = 15, pos = [0, 0], sf = 0.25, ori = self.target)
        
    def startStimulus(self, **kwargs):
        
        # Stimulus offset
        if self.target == self.rightTarget:
            self.grating.setPos([2.5,0])
        elif self.target == self.leftTarget:
            self.grating.setPos([-2.5,0])
            
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.grating.setOpacity(1)
        self.stimulusWindow.update()
        
    # Draw and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            if self.target == self.rightTarget:
                self.grating.setPhase(0.025, '+')  # move phase by 0.05 of a cycle
            elif self.target == self.leftTarget:
                self.grating.setPhase(0.025, '-')  # move phase by 0.05 of a cycle
            self.grating.draw()
            self.stimulusWindow.update()
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.grating.setOpacity(0)
        self.stimulusWindow.update()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()