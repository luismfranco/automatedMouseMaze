"""
Modules

"""

# GUI modules
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from PIL import ImageTk, Image
import os
import cv2

# Data modules
import time
import pandas as pd


""" 
Crown Cameras

"""

class crownCameras:
    
    def __init__(self, cameraIDs, pathForSavingData, sessionInfo):
        
        # Path
        self.pathForSavingData = pathForSavingData
        
        # Save data
        self.fileExtension = ".pickle "
        
        # Experiment data
        self.animalID = sessionInfo[0]
        self.currentDate = sessionInfo[1]
        self.blockID = sessionInfo[2]
        
        # Frame rate
        frameRate = 100                                  # (Hz). True frame rate must estimated. Delays are caused by other computations in the code and camera limitations
        self.cameraTimeBetweenFrames = 1000/frameRate    # miliseconds betweem frames
        
        # Initialize camera booleans
        self.camerasAreOn = False
        self.saveVideo = False
        self.okToSaveVideoFiles = False
        self.noVideoRecorded = True
        
        # Cameras
        self.eyeCameraID = cameraIDs[0]
        self.worldCameraID = cameraIDs[1]
        
        # Check if cameras are available
        self.eyeCameraAvailable = self.checkIfCameraIsAvailable(self.eyeCameraID, "eye")
        self.worldCameraAvailable = self.checkIfCameraIsAvailable(self.worldCameraID, "world")
        
        # If both cameras are available, initialize cameras
        if self.eyeCameraAvailable is True and self.worldCameraAvailable is True:
            
            # Initialize camera data
            self.cameraTimeStamps = []
            self.eyeCamRet = None
            self.worldCamRet = None
            self.eyeCamFrame = None
            self.worldCamFrame = None
            
            # Initialize camera objects    
            self.eyeCamera = cv2.VideoCapture(self.eyeCameraID) 
            self.worldCamera = cv2.VideoCapture(self.worldCameraID)  
            
            # Create window
            self.cameraWindow = tk.Toplevel()
            self.cameraWindow.title("Cameras")
              
            # Camera resolution. Convert from float to integer
            frameWidth = int(self.eyeCamera.get(3)) 
            frameHeight = int(self.eyeCamera.get(4)) 
            eyeCamSize = (frameWidth, frameHeight) 
            frameWidth = int(self.worldCamera.get(3)) 
            frameHeight = int(self.worldCamera.get(4)) 
            worldCamSize = (frameWidth, frameHeight) 
    
            # Canvas
            self.canvas = tk.Canvas(self.cameraWindow, width = eyeCamSize[0], height = eyeCamSize[1] + worldCamSize[1])
            self.canvas.pack()
            self.combinedFrame = None
            self.canvasImage = self.canvas.create_image(0, 0, image = self.combinedFrame, anchor = tk.NW)
    
            # Window
            windowWidth = eyeCamSize[0]
            windowHeight = eyeCamSize[1] + worldCamSize[1]
            screenWidth = self.cameraWindow.winfo_screenwidth()
            screenHeight = self.cameraWindow.winfo_screenheight()
            x = (screenWidth/5) - (windowWidth/2)
            y = (screenHeight/2.15) - (windowHeight/2)
            self.cameraWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
    
            # Check for existing video files
            fileName1 = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "eyeCamera" + "_" + str(self.blockID) + ".avi"
            fileName2 = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "worldCamera" + "_" + str(self.blockID) + ".avi"
            if not os.path.isfile(fileName1) and not os.path.isfile(fileName2):
                self.okToSaveVideoFiles = True
            else:
                self.okToSaveVideoFiles = messagebox.askyesno("Existing file", "Do you want to overwrite video files?", parent = self.cameraWindow)
            
            # Prepare video files
            if self.okToSaveVideoFiles is True:
                self.camerasAreOn = True
                self.eyeCameraVideo = cv2.VideoWriter(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "eyeCamera" + "_" + str(self.blockID) + ".avi",
                                                      cv2.VideoWriter_fourcc(*'MJPG'), 10, eyeCamSize)
                self.worldCameraVideo = cv2.VideoWriter(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "worldCamera" + "_" + str(self.blockID) + ".avi",
                                                        cv2.VideoWriter_fourcc(*'MJPG'), 10, worldCamSize)
            # Destroy camera window
            elif self.okToSaveVideoFiles is False:
                messagebox.showwarning("Video recording", "Please choose a different block number for you experiment." +
                                                          "\n" +
                                                          "\nThe current block number already exists.",
                                                          parent = self.cameraWindow)
                self.resetCameras()
                
        elif self.eyeCameraAvailable is False and self.worldCameraAvailable is False:
            
            print("Cameras are not available.")
            
        else:
            
            print("At least one camera is not available.")
        
    def checkIfCameraIsAvailable(self, cameraID, name):
        
        camera = cv2.VideoCapture(cameraID) 
        isCameraAvailable = camera.isOpened()
        if isCameraAvailable is False:
            print("Error reading " + name + " camera. Camera is not available.") 
        return isCameraAvailable
    
    def startCameras(self):
        
        if self.camerasAreOn is True:
            
            # Start cameras
            cameraThread = Thread(target = self.updateCameras)
            cameraThread.start()
            
            # Camera window
            self.cameraWindow.protocol('WM_DELETE_WINDOW', self.closeCameras)
            self.cameraWindow.mainloop()
            
    def recordVideo(self):
        
        if self.camerasAreOn is True:
            
            # Turning saving frames on
            self.saveVideo = True
            self.noVideoRecorded = False
        
    def stopVideo(self):
        
        if self.saveVideo is True:
            
            # Turning saving frames off
            self.saveVideo = False
            
        else:
            
            messagebox.showinfo("Cameras", "There is no ongoing video recording.", parent = self.cameraWindow)
        
    def updateCameras(self):
        
        if self.camerasAreOn is True:
        
            # Grab frame
            self.eyeCamRet, self.eyeCamFrame = self.eyeCamera.read()
            self.worldCamRet, self.worldCamFrame = self.worldCamera.read()
            self.cameraTimeStamps.append(time.time())
            
            if self.eyeCamRet is True or self.worldCamRet is True:
                
                # Save frame to video file
                if self.saveVideo is True:
                    self.eyeCameraVideo.write(self.eyeCamFrame)
                    self.worldCameraVideo.write(self.worldCamFrame)
                
                # Update frame to display
                self.combinedFrame = cv2.vconcat([self.worldCamFrame, self.eyeCamFrame])
                self.combinedFrame = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(self.combinedFrame, cv2.COLOR_BGR2RGB)))
                self.canvas.itemconfig(self.canvasImage, image = self.combinedFrame)
                
            # Loop
            self.cameraWindow.after(int(self.cameraTimeBetweenFrames), self.updateCameras)
        
    def closeCameras(self):
        
        if self.camerasAreOn is True:
            
            # Stop grabing frames and close window
            self.camerasAreOn = False
            self.saveVideo = False
            self.cameraWindow.after(50, self.resetCameras)
        
        return self.camerasAreOn, self.saveVideo
        
    def resetCameras(self):
        
        # Stop camera objects
        self.eyeCamera.release() 
        self.worldCamera.release()
        
        # Stop video files
        if self.okToSaveVideoFiles is True:
            
            # Close video files
            self.eyeCameraVideo.release() 
            self.worldCameraVideo.release()
            
            # If frames were not recorded, destroy video files
            if self.noVideoRecorded is True:
                os.remove(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "eyeCamera" + "_" + str(self.blockID) + ".avi")
                os.remove(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "worldCamera" + "_" + str(self.blockID) + ".avi")
                
            # If frames were recorded, save time stamps
            if self.noVideoRecorded is False:
                data = {
                        "rawCameraTimeStamps": self.cameraTimeStamps,
                                                                     }
                df = pd.DataFrame.from_dict(data, orient = 'index')
                df = df.transpose()    
                fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "cameraTimeStamps" + "_" + str(self.blockID)
                df.to_pickle(fileName + self.fileExtension)
            
        # Closes all the frames 
        cv2.destroyAllWindows() 
        
        # Destroy camera window
        self.cameraWindow.destroy()
    
        
"""
Main Block

"""

if __name__ == "__main__":
    crownCameras = crownCameras.__init__()