"""
Modules

"""

# Open Ephys modules
import subprocess
from open_ephys.control import OpenEphysHTTPServer

# Data module
import time


""" 
Open Ephys

"""

class openEphys:
    
    def __init__(self, OpenEphysPath, pathForSavingData, sessionInfo):
        
        # Experiment data
        animalID = sessionInfo[0]
        currentDate = sessionInfo[1]
        blockID = sessionInfo[2]
            
        # Launch Open Ephys GUI
        subprocess.Popen(OpenEphysPath)
        
        # Communicate with Open Ephys HTTP Server
        GUIstatus = []
        while GUIstatus != "connected":
            try:
                self.OpenEphysGUI = OpenEphysHTTPServer()
                if self.OpenEphysGUI.status() == "IDLE":
                    self.OpenEphysGUIHasBeenLaunched = True
                    GUIstatus = "connected"
            except:
                time.sleep(1)
        
        # Set Open Ephys booleans
        self.ephysPreviewIsOn = False
        self.ephysRecordingInProgress = False
        
        # Path and data file name
        self.OpenEphysGUI.set_start_new_dir()
        self.OpenEphysGUI.set_parent_dir(pathForSavingData)
        self.OpenEphysGUI.set_prepend_text(animalID + "_")
        self.OpenEphysGUI.set_base_text(currentDate)
        self.OpenEphysGUI.set_append_text("_" + "ephysData" + "_" + str(blockID))
        recordNodeID = self.OpenEphysGUI.get_recording_info(key = "record_nodes")
        recordNodeID = recordNodeID[0]["node_id"]
        self.OpenEphysGUI.send("/api/recording/" + str(recordNodeID), payload = {'parent_directory' : pathForSavingData})
            
    def previewOpenEphysChannels(self):
        
        if self.OpenEphysGUIHasBeenLaunched is True and self.ephysPreviewIsOn is False and self.ephysRecordingInProgress is False:
            
            # Start preview mode
            self.OpenEphysGUI.acquire()
            self.ephysPreviewIsOn = True
            
        elif self.OpenEphysGUIHasBeenLaunched is True and self.ephysPreviewIsOn is True and self.ephysRecordingInProgress is False:
            
            # Stop preview mode
            self.OpenEphysGUI.idle()
            self.ephysPreviewIsOn = False
            
        elif self.ephysRecordingInProgress is True:
            print("There is an ongoing recording in progress.")
            
    def startEphysRecording(self):
        
        if self.OpenEphysGUIHasBeenLaunched is True and self.ephysRecordingInProgress is False:
            
            # Start recording
            self.OpenEphysGUI.record()
            self.ephysRecordingInProgress = True
        
    def stopEphysRecording(self):
        
        if self.OpenEphysGUIHasBeenLaunched is True and self.ephysRecordingInProgress is True:
            
            # Stop recording
            self.OpenEphysGUI.idle()
            self.ephysRecordingInProgress = False
            
        elif self.ephysRecordingInProgress is False:
            print("No recording in progress.")
        
    def closeOpenEphysGUI(self):
    
        if self.OpenEphysGUIHasBeenLaunched is True and self.ephysPreviewIsOn is False and self.ephysRecordingInProgress is False:
            
            # Close Open Ephys GUI
            self.OpenEphysGUI.quit()
            self.OpenEphysGUIHasBeenLaunched = False
            
        elif self.ephysPreviewIsOn is True:
            print("Open Ephys is currently in preview mode.")
            
        elif self.ephysRecordingInProgress is True:
            print("There is an ongoing recording in progress.")
            
            
"""
Main Block

"""

if __name__ == "__main__":
    openEphys = openEphys.__init__()