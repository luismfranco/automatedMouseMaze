"""
Modules

"""

# GUI modules
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from threading import Thread
from PIL import ImageTk, Image
import os
from datetime import datetime
from pathlib import Path

# Connectivity
import socket
import select

# Crown cameras
import crownCameras

# Open Ephys
import openEphys

# Data modules
import time
import ntplib
import pickle
import pandas as pd


"""
Application

"""

class acquisitionGUI:
    
    
    """
    Set up GUI

    """
    
    def __init__(self, mainWindow, configurationData):
        
        
        """
        GUI Layout
        
        """
        
        # Geometry and location
        self.mainWindow = mainWindow
        self.mainWindow.title('Acquisition Control Panel')
        windowWidth = 500
        windowHeight = 600
        screenWidth = self.mainWindow.winfo_screenwidth()
        screenHeight = self.mainWindow.winfo_screenheight()
        x = (screenWidth/1.25) - (windowWidth/2)
        y = (screenHeight/2) - (windowHeight/2)
        self.mainWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.backGroundColor = self.mainWindow.cget('bg')
        buttonFont = tkFont.Font(family = 'helvetica', size = 12)
        
        # Frame 1: Logo
        frame1 = tk.Frame(self.mainWindow, width = 500, height = 100)
        frame1.place(anchor = "c", relx = 0.5, rely = 0.11)
        
        # Frame 2: Connection with Maze GUI
        frame2 = tk.Frame(self.mainWindow, width = 500, height = 100)
        frame2.place(anchor = "c", relx = 0.5, rely = 0.28)
        
        # Frame 3: Crown camera controls
        frame3 = tk.Frame(self.mainWindow, width = 250, height = 350)
        frame3.place(anchor = "c", relx = 0.25, rely = 0.62)
        
        # Frame 4: Open Ephys controls
        frame4 = tk.Frame(self.mainWindow, width = 250, height = 350)
        frame4.place(anchor = "c", relx = 0.75, rely = 0.62)
        
        # Frame 5: Open Ephys controls
        frame5 = tk.Frame(self.mainWindow, width = 500, height = 50)
        frame5.place(anchor = "c", relx = 0.5, rely = 0.935)
        
        # Logo
        imagePath = "assets/mazeGUIlogo.png"
        img = Image.open(imagePath)
        img = img.resize((280, 100))
        self.img = ImageTk.PhotoImage(master = frame1, width = 280, height = 100, image = img)
        logo = tk.Label(frame1, image = self.img)
        logo.place(anchor = "c", relx = 0.5, rely = 0.5)
        
        # Save data
        self.fileExtension = ".pickle "
        
        
        """
        Session Info
        
        """
        
        self.animalID = "J700NC"
        self.currentDate = "250101"
        self.blockID = "1"
        userName = os.getlogin()
        self.currentDate = datetime.today().strftime("%y%m%d")
        self.pathForSavingData = "C:\\Users\\" + userName + "\\Documents\\automatedMouseMaze\\Data\\" + self.currentDate + "\\"        
        Path(self.pathForSavingData).mkdir(parents = True, exist_ok = True)
        
        
        """
        Connection with Maze GUI
        
        """
        
        # Maze GUI controls
        self.mazeGUIaddress = configurationData["acquisitionControlPanel"]["mazeGUIaddress"]
        self.acquisitionPanelConnection = False
        self.aRecordingWasStarted = False        
        
        # Connection label
        tk.Label(frame2, font = buttonFont, text = "Maze GUI Connection", width = 25, anchor  = 'c').grid(row = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'we')
        
        # Start connection
        self.startConnectionButton = tk.Button(frame2, text = 'Connect', font = buttonFont, width = 17, command = self.startConnection)
        self.startConnectionButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.startConnectionButton.bind('<Enter>', lambda e: self.startConnectionButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.startConnectionButton.bind('<Leave>', lambda e: self.startConnectionButton.config(fg = 'Black', bg ='SystemButtonFace'))

        # Close connection
        self.closeConnectionButton = tk.Button(frame2, text = 'Disconnect', font = buttonFont, width = 17, command = self.closeConnection)
        self.closeConnectionButton.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.closeConnectionButton.bind('<Enter>', lambda e: self.closeConnectionButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.closeConnectionButton.bind('<Leave>', lambda e: self.closeConnectionButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Save button
        self.saveButton = tk.Button(frame5, text = 'Save Offsets', font = buttonFont, width = 17, command = self.saveTimeStampOffsets)
        self.saveButton.grid(row = 1, column = 0,padx = 10, pady = 10)
        self.saveButton.bind('<Enter>', lambda e: self.saveButton.config(fg='Black', bg='#84E0E0'))
        self.saveButton.bind('<Leave>', lambda e: self.saveButton.config(fg='Black', bg='SystemButtonFace'))
        
        # Close app button
        self.closeButton = tk.Button(frame5, text = 'Close', font = buttonFont, width = 17, command = self.closeMainWindow)
        self.closeButton.grid(row = 1, column = 1,padx = 10, pady = 10)
        self.closeButton.bind('<Enter>', lambda e: self.closeButton.config(fg='Black', bg='#AFAFAA'))
        self.closeButton.bind('<Leave>', lambda e: self.closeButton.config(fg='Black', bg='SystemButtonFace'))
        self.mainWindow.protocol('WM_DELETE_WINDOW', self.closeMainWindow)
        
        
        """
        Camera Controls
        
        """
        
        # Cameras
        eyeCameraID = int(configurationData["crownCameras"]["eyeCamera"])
        worldCameraID = int(configurationData["crownCameras"]["worldCamera"])
        self.cameraIDs = [eyeCameraID, worldCameraID]
        
        # Camera labels
        self.cameraPanelLabel = tk.Label(frame3, font = buttonFont, text = "Camera Controls", width = 25, anchor  = 'c')
        self.cameraPanelLabel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'we')
        
        # Initialize cameras
        self.startCameraButton = tk.Button(frame3, text = 'Start Cameras', font = buttonFont, width = 17, command = self.startCameras)
        self.startCameraButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))

        # Start recording
        self.recordCameraButton = tk.Button(frame3, text = 'Record Video', font = buttonFont, width = 17, command = self.recordVideo)
        self.recordCameraButton.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
        self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Stop recording
        self.stopRecordCameraButton = tk.Button(frame3, text = 'Stop Recording', font = buttonFont, width = 17, command = self.stopVideo)
        self.stopRecordCameraButton.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.stopRecordCameraButton.bind('<Enter>', lambda e: self.stopRecordCameraButton.config(fg = 'Black', bg ='#FFB844'))
        self.stopRecordCameraButton.bind('<Leave>', lambda e: self.stopRecordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))

        # Close cameras
        self.closeCameraButton = tk.Button(frame3, text = 'Close Cameras', font = buttonFont, width = 17, command = self.closeCameras)
        self.closeCameraButton.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.closeCameraButton.bind('<Enter>', lambda e: self.closeCameraButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.closeCameraButton.bind('<Leave>', lambda e: self.closeCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        
        """
        Open Ephys Controls
        
        """
        
        # Path for Open Ephys exe
        self.OpenEphysPath = configurationData["openEphys"]["openEphysPath"]
        
        # Open Ephys labels
        self.EphysPanelLabel = tk.Label(frame4, font = buttonFont, text = "Ephys and IMU Controls", width = 25, anchor  = 'c')
        self.EphysPanelLabel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'we')
        
        # Initialize Open Ephys GUI
        self.launchOpenEphysButton = tk.Button(frame4, text = 'Launch Open Ephys', font = buttonFont, width = 17, command = self.launchOpenEphysGUI)
        self.launchOpenEphysButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.launchOpenEphysButton.bind('<Enter>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.launchOpenEphysButton.bind('<Leave>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Preview
        self.previewOpenEphysButton = tk.Button(frame4, text = 'Preview Off', font = buttonFont, width = 17, command = self.previewOpenEphysChannels)
        self.previewOpenEphysButton.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='#99D492'))
        self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Start recording
        self.startEphysRecordingButton = tk.Button(frame4, text = 'Start Recording', font = buttonFont, width = 17, command = self.startEphysRecording)
        self.startEphysRecordingButton.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.startEphysRecordingButton.bind('<Enter>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='#DC5B5B'))
        self.startEphysRecordingButton.bind('<Leave>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Stop recording
        self.stopEphysRecordingButton = tk.Button(frame4, text = 'Stop Recording', font = buttonFont, width = 17, command = self.stopEphysRecording)
        self.stopEphysRecordingButton.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.stopEphysRecordingButton.bind('<Enter>', lambda e: self.stopEphysRecordingButton.config(fg = 'Black', bg ='#FFB844'))
        self.stopEphysRecordingButton.bind('<Leave>', lambda e: self.stopEphysRecordingButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Close Open Ephys GUI
        self.closeOpenEphysGUIButton = tk.Button(frame4, text = 'Close Open Ephys', font = buttonFont, width = 17, command = self.closeOpenEphysGUI)
        self.closeOpenEphysGUIButton.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.closeOpenEphysGUIButton.bind('<Enter>', lambda e: self.closeOpenEphysGUIButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.closeOpenEphysGUIButton.bind('<Leave>', lambda e: self.closeOpenEphysGUIButton.config(fg = 'Black', bg ='SystemButtonFace'))


    """ 
    Connection Functions
    
    """
    
    def startConnection(self):
        
        if self.acquisitionPanelConnection is False:

            # Update startCameraButton: connection with client established...
            self.startConnectionButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Connected')
            self.startConnectionButton.bind('<Enter>', lambda e: self.startConnectionButton.config(fg = 'Blue', bg ='#A9C6E3'))
            self.startConnectionButton.bind('<Leave>', lambda e: self.startConnectionButton.config(fg = 'Blue', bg = '#A9C6E3'))
            self.startConnectionButton.update_idletasks()
            
            # Disable all acquisition buttons and labels
            buttonNames = [self.cameraPanelLabel, self.startCameraButton, self.recordCameraButton, self.stopRecordCameraButton, self.closeCameraButton,
                           self.EphysPanelLabel, self.launchOpenEphysButton, self.previewOpenEphysButton, self.startEphysRecordingButton, self.stopEphysRecordingButton, self.closeOpenEphysGUIButton]
            for i in range(len(buttonNames)):
                buttonNames[i].config(state = "disabled")
                buttonNames[i].update_idletasks()
            
            # Start Acquisition Panel socket (server)
            self.server = socket.socket()
            # self.server.bind(('127.0.0.1', 12345))
            self.server.bind((self.mazeGUIaddress, 12345))
            self.server.listen(1)
            print("Acquisition Panel is listening. Waiting for maze GUI to connect...")
            (self.client, clientAddress) = self.server.accept()
            print("Acquisition Panel connected to: ", str(clientAddress[0]))
            self.server.setblocking(False)
            self.acquisitionPanelConnection = True
            
            # Start checking on Maze GUI (client)
            self.clientCommand = []
            self.clientData = []
            self.dataForClient = []
            self.notifyClient = True
            
            # Thread to handle listening to Maze GUI (client)
            connectionThread = Thread(target = self.checkOnClient)
            connectionThread.start()

        elif self.acquisitionPanelConnection is True:
            
            print("Connection with Maze GUI has been already established.")
    
    def resetTimeStamps(self):
        
        # Data synchronization
        self.timeServer = ntplib.NTPClient()
        self.aRecordingWasStarted = False
        self.timeStampOffest = None
        self.timeStamp = None
        self.dataFrameTimeStampOffset = []
        self.dataFrameTimeStamp = []
    
    def startCameraFeed(self):
        
        if self.cameraFeedStarted is False:
            if self.clientCommand == "startCameras":
                self.cameraFeedStarted = True
                self.crownCameras.startCameras()
            self.mainWindow.after(100, self.startCameraFeed)
    
    def updateClientCommand(self):
    
        # Crown Cameras
        if self.clientCommand == "cameraInput":
            # Experiment data
            self.cameraIDs = self.clientData[0]
            self.sessionInfo = self.clientData[1]
            self.animalID, self.currentDate, self.blockID = self.clientData[1]
            self.clientData = []
            print("Acquisition Panel received experimental session data.")
        elif self.clientCommand == "initializeCameras":
            # Thread to handle starting camera feed
            if self.aRecordingWasStarted is False:
                self.resetTimeStamps()
            elif self.aRecordingWasStarted is True:
                print("A recording was previously started. Please save data before starting a new recording.")
            self.cameraFeedStarted = False
            cameraFeed = Thread(target = self.startCameraFeed)
            cameraFeed.start()
            # Initialize cameras
            try:
                self.crownCameras = crownCameras.crownCameras(self.cameraIDs, self.pathForSavingData , self.sessionInfo)
                dataForClient = [self.crownCameras.camerasAreOn, self.crownCameras.eyeCameraAvailable, self.crownCameras.worldCameraAvailable]
                self.dataForClient = pickle.dumps(dataForClient)
                print("Crown Cameras have been initialized.")
            except:
                print("Crown Cameras could not be initialized. Most likely a file with the same name already exists.")
        elif self.clientCommand == "recordVideo":
            # Start recording
            self.aRecordingWasStarted = True
            self.crownCameras.recordVideo()
            dataForClient = [self.crownCameras.saveVideo]
            self.dataForClient = pickle.dumps(dataForClient)
            print("Video recording in progress...")
        elif self.clientCommand == "stopVideo":
            # Stop recording
            self.crownCameras.stopVideo()
            dataForClient = [self.crownCameras.saveVideo]
            self.dataForClient = pickle.dumps(dataForClient)
            print("Video recording stopped.")
        elif self.clientCommand == "closeCameras":
            # Close cameras
            self.crownCameras.closeCameras()
            dataForClient = [self.crownCameras.camerasAreOn, self.crownCameras.saveVideo]
            self.dataForClient = pickle.dumps(dataForClient)
            del self.crownCameras
            self.cameraFeedStarted = False
            if self.aRecordingWasStarted is True:
                self.saveTimeStampOffsets()
            print("Crown Cameras have been closed.")
        elif self.clientCommand == "deleteCameras":
            # Delete camera object
            del self.crownCameras
            
        # Open Ephys
        elif self.clientCommand == "launchOpenEphys":
            # Experiment data
            self.sessionInfo = self.clientData[0]
            self.animalID, self.currentDate, self.blockID = self.clientData[0]
            self.clientData = []
            print("Acquisition Panel received experimental session data.")
            # Launch Open Ephys GUI
            if self.aRecordingWasStarted is False:
                self.resetTimeStamps()
            elif self.aRecordingWasStarted is True:
                print("A recording was previously started. Please save data before starting a new recording.")
            self.openEphys = openEphys.openEphys(self.OpenEphysPath, self.pathForSavingData , self.sessionInfo)
            dataForClient = [self.openEphys.OpenEphysGUIHasBeenLaunched, self.openEphys.ephysPreviewIsOn, self.openEphys.ephysRecordingInProgress]
            self.dataForClient = pickle.dumps(dataForClient)            
            print("Open Ephys GUI has been launched.")
        elif self.clientCommand == "previewOpenEphysChannels":
            # Start/stop ephys preview
            self.openEphys.previewOpenEphysChannels()
            dataForClient = [self.openEphys.ephysPreviewIsOn]
            self.dataForClient = pickle.dumps(dataForClient)
            if self.openEphys.ephysPreviewIsOn is True:
                print("Open Ephys preview mode is on.")
            elif self.openEphys.ephysPreviewIsOn is False:
                print("Open Ephys preview mode is off.")
        elif self.clientCommand == "startEphysRecording":
            # Start recording
            self.aRecordingWasStarted = True
            self.openEphys.startEphysRecording()
            dataForClient = [self.openEphys.ephysRecordingInProgress]
            self.dataForClient = pickle.dumps(dataForClient)
            print("Ephys recording in progress...")
        elif self.clientCommand == "stopEphysRecording":
            # Stop recording
            self.openEphys.stopEphysRecording()
            dataForClient = [self.openEphys.ephysRecordingInProgress]
            self.dataForClient = pickle.dumps(dataForClient)
            print("Ephys recording stopped.")
        elif self.clientCommand == "closeOpenEphys":
            # Close Open Ephys GUI
            self.openEphys.closeOpenEphysGUI()
            dataForClient = [self.openEphys.OpenEphysGUIHasBeenLaunched]
            self.dataForClient = pickle.dumps(dataForClient)
            del self.openEphys
            print("Open Ephys GUI has been closed.")
        
        # Time synchronization
        elif self.clientCommand == "grabTimeOffset":
            try:
                self.timeStampOffest = self.timeServer.request('pool.ntp.org').offset
            except:
                self.timeStampOffest = None
            self.timeStamp = time.time()
            self.dataFrameTimeStampOffset.append(self.timeStampOffest)
            self.dataFrameTimeStamp.append(self.timeStamp)
        
        # Connection with Maze GUI
        elif self.clientCommand == "closeConnection":
            self.notifyClient = self.clientData[0]
            self.closeConnection()
            
    def checkOnClient(self):
        
        if self.acquisitionPanelConnection is True:
            
            # Read data from Maze GUI (client)
            listenToClient, _, _ = select.select([self.client], [], [], 0.05)
            for s in listenToClient:
                if s == self.client:
                    data = s.recv(1024)
                    if data:
                        try:
                            clientData = pickle.loads(data)
                            self.clientCommand = clientData[0]
                            if len(clientData) > 1:
                                self.clientData = clientData[1:]
                            self.updateClientCommand()
                        except pickle.UnpicklingError:
                            print("Error processing client data.")
            
            # Send data to Maze GUI (client)
            if self.dataForClient:
                self.client.send(self.dataForClient)
                self.dataForClient = []
            
            # Loop
            self.mainWindow.after(100, self.checkOnClient)
        
    def closeConnection(self):
        
        if self.acquisitionPanelConnection is True:
            
            # Notify Maze GUI (client)
            if self.notifyClient is True:
                dataForClient = ["closeConnection"]
                self.dataForClient = pickle.dumps(dataForClient)
                self.client.send(self.dataForClient)
            
            # Close Acquisition Panel socket (server)
            self.server.close()
            self.acquisitionPanelConnection = False
            print("Connection with Maze GUI has now been been closed.")
            
            # Reset startConnectionButton
            self.startConnectionButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Connect')
            self.startConnectionButton.bind('<Enter>', lambda e: self.startConnectionButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.startConnectionButton.bind('<Leave>', lambda e: self.startConnectionButton.config(fg = 'Black', bg = 'SystemButtonFace'))
            self.startConnectionButton.update_idletasks()
            
            # Enable all acquisition buttons
            buttonNames = [self.cameraPanelLabel, self.startCameraButton, self.recordCameraButton, self.stopRecordCameraButton, self.closeCameraButton,
                           self.EphysPanelLabel, self.launchOpenEphysButton, self.previewOpenEphysButton, self.startEphysRecordingButton, self.stopEphysRecordingButton, self.closeOpenEphysGUIButton]
            for i in range(len(buttonNames)):
                buttonNames[i].config(state = "normal")
                buttonNames[i].update_idletasks()
            
        elif self.acquisitionPanelConnection is False:
            
            print("Connection with Maze GUI has not been established yet.")
    
    
    """ 
    Crown Camera Functions
    
    """

    def startCameras(self):
        
        try:
            
            self.crownCameras
        
        except:
            
            # Update startCameraButton: starting cameras...
            self.startCameraButton.config(fg = 'Black', bg = '#A9C6E3', text = 'Starting...', relief = 'sunken')
            self.startCameraButton.update_idletasks()
            
            # Experiment data
            experimentData = [self.animalID, self.currentDate, self.blockID]
            
            # Initialize crown cameras
            self.crownCameras = crownCameras.crownCameras(self.cameraIDs, self.pathForSavingData , experimentData)

            if self.crownCameras.eyeCameraAvailable is True and self.crownCameras.worldCameraAvailable is True:
                
                if self.crownCameras.camerasAreOn is True:
                    
                    # Update startCameraButton: cameras are open (preview mode)...
                    self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Preview')
                    self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Blue', bg ='#A9C6E3'))
                    self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3'))
                    self.startCameraButton.update_idletasks()
                    
                    # Start camera feed (preview)
                    self.crownCameras.startCameras()
                    
                elif self.crownCameras.camerasAreOn is False:
                    
                    # Reset startCameraButton
                    self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
                    self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                    self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                    self.startCameraButton.update_idletasks()
                    
                    # Delete camera object
                    del self.crownCameras
                
            else:
                
                # Reset startCameraButton
                self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
                self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.startCameraButton.update_idletasks()
                    
                # Delete camera object    
                del self.crownCameras
                
        else:
            
            print("Cameras are already in use.")
        
    def recordVideo(self):
        
        try:
            
            self.crownCameras
        
        except:
            
            messagebox.showinfo("Cameras", "Cameras have not been started yet.", parent = self.mainWindow)
            
        else:
            
            if self.crownCameras.camerasAreOn is True:
                
                # Update camera buttons. Recording video...
                self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
                self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.startCameraButton.update_idletasks()
                self.recordCameraButton.config(fg = 'Black', bg = '#DC5B5B', relief = 'sunken', text = 'Recording')
                self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
                self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg = '#DC5B5B'))
                self.recordCameraButton.update_idletasks()
                
            # Start video recording
            self.aRecordingWasStarted = True
            self.crownCameras.recordVideo()
        
    def stopVideo(self):
        
        try:
            
            self.crownCameras
        
        except:
            
            messagebox.showinfo("Cameras", "Cameras have not been started yet.", parent = self.mainWindow)
            
        else:
            
            if self.crownCameras.saveVideo is True:
                
                # Update recordCameraButton: stop video recording...
                self.recordCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Record Video')
                self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg = 'SystemButtonFace'))
                self.recordCameraButton.update_idletasks()
                
            # Stop video recording    
            self.crownCameras.stopVideo()
        
    def closeCameras(self):
        
        try:
            
            self.crownCameras
        
        except:
            
            messagebox.showinfo("Cameras", "Cameras have not been started yet.", parent = self.mainWindow)
            
        else:
            
            if self.crownCameras.camerasAreOn is True:
                
                # Reset camera buttons
                self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
                self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.startCameraButton.update_idletasks()
                self.recordCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Record Video')
                self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
                self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.recordCameraButton.update_idletasks()
    
                # Close crown cameras
                self.crownCameras.closeCameras()
                
            # Delete camera object
            del self.crownCameras


    """ 
    Open Ephys Functions
    
    """
    
    def launchOpenEphysGUI(self):
        
        try:
            
            self.openEphys
            
        except:
            
            # Experiment data
            sessionInfo = [self.animalID, self.currentDate, self.blockID]    
        
            # Launch Open Ephys GUI locally
            self.openEphys = openEphys.openEphys(self.OpenEphysPath, self.pathForSavingData , sessionInfo)
                
            if self.openEphys.OpenEphysGUIHasBeenLaunched is True:
                
                # Update launchOpenEphysButton: GUI has been launched...
                self.launchOpenEphysButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Launched')
                self.launchOpenEphysButton.bind('<Enter>', lambda e: self.launchOpenEphysButton.config(fg = 'Blue', bg ='#A9C6E3'))
                self.launchOpenEphysButton.bind('<Leave>', lambda e: self.launchOpenEphysButton.config(fg = 'Blue', bg = '#A9C6E3'))
                self.launchOpenEphysButton.update_idletasks()        
        
        else:
        
            print("Open Ephys GUI has been already launched.")
            
    def previewOpenEphysChannels(self):
        
        try:
            
            self.openEphys
        
        except:
            
            messagebox.showinfo("Open Ephys GUI", "Open Ephys GUI has not been laucnhed yet.", parent = self.mainWindow)
            
        else:
            
            if self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysPreviewIsOn is False and self.openEphys.ephysRecordingInProgress is False:
                
                # Update previewOpenEphysButton: preview mode...
                self.previewOpenEphysButton.config(fg = 'Black', bg = '#99D492', relief = 'sunken', text = 'Preview On')
                self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Blue', bg ='#99D492'))
                self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Blue', bg = '#99D492'))
                self.previewOpenEphysButton.update_idletasks()
                
                # Start preview mode
                self.openEphys.previewOpenEphysChannels()
            
            elif self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysPreviewIsOn is True and self.openEphys.ephysRecordingInProgress is False:
                
                # Update previewOpenEphysButton: preview mode...
                self.previewOpenEphysButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Preview Off')
                self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='#99D492'))
                self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg = 'SystemButtonFace'))
                self.previewOpenEphysButton.update_idletasks()
                
                # Stop preview mode
                self.openEphys.previewOpenEphysChannels()
            
    def startEphysRecording(self):
        
        try:
            
            self.openEphys
        
        except:
            
            messagebox.showinfo("Open Ephys GUI", "Open Ephys GUI has not been laucnhed yet.", parent = self.mainWindow)
            
        else:
            
            if self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysRecordingInProgress is False:
                
                # Update previewOpenEphysButton: preview mode...
                if self.openEphys.ephysPreviewIsOn is True:
                    self.previewOpenEphysButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Preview Off')
                    self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='#99D492'))
                    self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg = 'SystemButtonFace'))
                    self.previewOpenEphysButton.update_idletasks()
                    
                # Update startEphysRecordingButton. Recording in progress...
                self.startEphysRecordingButton.config(fg = 'Black', bg = '#DC5B5B', relief = 'sunken', text = 'Recording')
                self.startEphysRecordingButton.bind('<Enter>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='#DC5B5B'))
                self.startEphysRecordingButton.bind('<Leave>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg = '#DC5B5B'))
                self.startEphysRecordingButton.update_idletasks()
                
                # Start ephys recording
                self.aRecordingWasStarted = True
                self.openEphys.startEphysRecording()
        
    def stopEphysRecording(self):
        
        try:
            
            self.openEphys
        
        except:
            
            messagebox.showinfo("Open Ephys GUI", "Open Ephys GUI has not been laucnhed yet.", parent = self.mainWindow)
            
        else:
            
            if self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysRecordingInProgress is True:
                
                # Update startEphysRecordingButton. Recording in progress...
                self.startEphysRecordingButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Recording')
                self.startEphysRecordingButton.bind('<Enter>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='#DC5B5B'))
                self.startEphysRecordingButton.bind('<Leave>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg = 'SystemButtonFace'))
                self.startEphysRecordingButton.update_idletasks()
                
                # Stop ephys recording
                self.openEphys.stopEphysRecording()
        
    def closeOpenEphysGUI(self):
        
        try:
            
            self.openEphys
        
        except:
            
            messagebox.showinfo("Open Ephys GUI", "Open Ephys GUI has not been laucnhed yet.", parent = self.mainWindow)
            
        else:
            
            if self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysPreviewIsOn is False and self.openEphys.ephysRecordingInProgress is False:
                
                # Update launchOpenEphysButton: GUI has been closed...
                self.launchOpenEphysButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Launch Open Ephys')
                self.launchOpenEphysButton.bind('<Enter>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.launchOpenEphysButton.bind('<Leave>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.launchOpenEphysButton.update_idletasks()
                
                # Close Open Ephys GUI
                self.openEphys.closeOpenEphysGUI()
                
                # Delete camera object
                del self.openEphys


    """ 
    App Buttons
    
    """
    
    def saveTimeStampOffsets(self):
        
        if self.aRecordingWasStarted is True:

            programStillRunning = False
            for name in ("self.crownCameras", "self.openEphys"):
                try:
                    exec(name)
                except:
                    ...
                else:
                    programStillRunning = True
    
            if programStillRunning is False:
                
                # Build dataFrame
                timeStamps = {
                        "timeOffset": self.dataFrameTimeStampOffset,
                        "timeStamps": self.dataFrameTimeStamp,
                                                                           }
                timeStamps = pd.DataFrame.from_dict(timeStamps, orient = 'index')
                timeStamps = timeStamps.transpose()
                
                # Save time stamps
                fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "timeStampOffsets" + "_" + str(self.blockID)
                if timeStamps.empty:
                    print("DataFrame is empty. Most likely an experiment has not been run yet.")
                else:
                    if not os.path.isfile(fileName + self.fileExtension):
                        timeStamps.to_pickle(fileName + self.fileExtension)
                        messagebox.showinfo("Data Saved", "Time offsets with maze have been saved at " + self.pathForSavingData)
                    else:
                        isNotSaved = True
                        while isNotSaved is True:
                            blockID = fileName[-1]
                            blockID = int(blockID)
                            blockID += 1
                            fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "timeStampOffsets" + "_" + str(blockID)
                            if not os.path.isfile(fileName + self.fileExtension):
                                timeStamps.to_pickle(fileName + self.fileExtension)
                                messagebox.showwarning("Data Saved", "Time offsets with maze have been saved at " + self.pathForSavingData +
                                                       "\n " +
                                                       "\nHowever, the block number was changed to " + str(blockID) + " to avoid overwriting existing file." +
                                                       "\n"
                                                       "\nIf video was recorded, make sure block numbers match.")
                                isNotSaved = False
                    print("Time stamps have been saved successfully.")
                    print(" ")
                    self.aRecordingWasStarted = False
                
            elif programStillRunning is True:
                
                messagebox.showinfo("No Data Saved", "The Crown Cameras and/or the Open Ephys GUI are still running." +
                                    "\n"
                                    "\nPlease close both programs before saving time stamps.")
        
    def closeMainWindow(self):
        
        # Kill GUI
        if self.acquisitionPanelConnection is False:
            self.mainWindow.destroy()
            self.mainWindow.quit()
            

"""
Main Block

"""

if __name__ == "__main__":
    acquisitionGUI = acquisitionGUI.__init__()