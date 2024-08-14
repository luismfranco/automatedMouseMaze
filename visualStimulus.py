
"""
Modules

"""

from psychopy import visual


"""
Drifting Gratings

"""

class driftingGratings:
    
    def __init__(self):
    
        # Create a window
        self.stimulusWindow = visual.Window([800,600], monitor = "testMonitor", units = "deg")
        
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
        self.grating = visual.GratingStim(win = self.stimulusWindow, mask = "circle", size = 10, pos = [0,0], sf = 1, ori = self.target)
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


"""
Object Discrimination

"""

class objectDiscrimination:
    
    def __inti__(self):
    
        # Create a window
        self.stimulusWindow = visual.Window([800,600], monitor = "testMonitor", units = "deg")
        
        # Which object for left or right?
        
        # Stimulus
        self.showVisualStimulus = False
        
        
        
        
        
        
        
        
        