"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from psychopy import visual


"""
Drifting Gratings

"""

class driftingGratings:
    
    def __init__(self, stimulusScreen):
    
        # Create a window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen, units = "deg",
                                            size = (1024, 600), fullscr = True, color = (1.0, 1.0, 1.0))
        
        # Orientation
        self.leftTarget = 90
        self.rightTarget = 0
        
        # Stimulus
        self.showVisualStimulus = False
        
    def startStimulus(self, **kwargs):
        
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.target = self.leftTarget
        elif self.targetLocation == 1:
            self.target = self.rightTarget
            
        # Stimulus
        self.grating = visual.GratingStim(win = self.stimulusWindow, mask = "raisedCos", size = 15, pos = [0,0], sf = 0.5, ori = self.target)
        self.grating.setOpacity(1)
        self.stimulusWindow.update()
        
    # Draw and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            
            if self.target == self.rightTarget:
                self.grating.setPhase(0.05, '+')  # move phase by 0.05 of a cycle
            elif self.target == self.leftTarget:
                self.grating.setPhase(0.05, '-')  # move phase by 0.05 of a cycle
            self.grating.draw()
            self.stimulusWindow.update()
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.grating.setOpacity(0)
        self.stimulusWindow.update()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()