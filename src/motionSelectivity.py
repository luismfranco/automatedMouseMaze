"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from psychopy import visual
from psychopy.visual.dot import DotStim


"""
Drifting Gratings

"""

class motionSelectivity:
    
    def __init__(self, stimulusScreen):
    
        # Create a window
        self.stimulusWindow = visual.Window(monitor = "testMonitor", screen = stimulusScreen-2, units = "deg",
                                            size = (1024, 600), color = (1.0, 1.0, 1.0)) # fullscr = True,
        
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
        self.movingDots = DotStim(win = self.stimulusWindow, nDots = 100, coherence = 0.65, dotSize = 12.5,
                                  dotLife = 60*5, speed = 0.05, color = 'black', contrast = 1.0, 
                                  dir = self.target, fieldSize = (15, 15), fieldShape = 'circle', noiseDots = 'direction')
        self.movingDots.setOpacity(1)
        self.stimulusWindow.update()
        
    # Draw and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            self.movingDots.draw()
            self.stimulusWindow.update()
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        self.movingDots.setOpacity(0)
        self.stimulusWindow.update()
    
    # Cleanup
    def closeWindow(self):
        
        self.stimulusWindow.close()