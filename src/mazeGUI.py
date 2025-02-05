"""
Modules

"""

# GUI modules
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox, ttk
from threading import Thread
from PIL import ImageTk, Image
import os
from datetime import datetime
from pathlib import Path
import cv2

# Teensy modules
import pyfirmata
import serial
import serial.tools.list_ports
import simpleaudio as sa

# Visual stimulus module
import driftingGratings
import motionSelectivity
import whiteNoise
import objectDiscrimination

# Valve calibration
import valveCalibration

# Data modules
import time
import numpy as np
import pandas as pd


"""
Application

"""

class mazeGUI:
    
    
    """
    Set up GUI

    """
    
    def __init__(self, mainWindow, configurationData):
        
        
        """
        GUI Layout
        
        """
        
        # Geometry
        self.mainWindow = mainWindow
        self.mainWindow.title('Automated Mouse Maze')
        windowWidth = 925
        windowHeight = 500
        screenWidth = self.mainWindow.winfo_screenwidth()
        screenHeight = self.mainWindow.winfo_screenheight()
        x = (screenWidth/1.5) - (windowWidth/2)
        y = (screenHeight/2) - (windowHeight/2)
        self.mainWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.backGroundColor = self.mainWindow.cget('bg')
        buttonFont = tkFont.Font(family = 'helvetica', size = 12)
        
        # Frames
        frame1 = tk.Frame(self.mainWindow, width = 225, height = 500) #, bg = 'green')
        frame1.grid(row = 0, rowspan = 3, column = 0, sticky = 'news')
        frame11 = tk.Frame(frame1, width = 225, height = 175)
        frame11.place(anchor = "c", relx = 0.5, rely = 0.175)
        frame12 = tk.Frame(frame1, width = 225, height = 325)
        frame12.place(anchor = "c", relx = 0.5, rely = 0.6)
        frame2 = tk.Frame(self.mainWindow, width = 500, height = 350) #, bg = 'red')
        frame2.grid(row = 0, rowspan = 2, column = 1, sticky = 'news')
        frame21 = tk.Frame(frame2, width = 500, height = 150)
        frame21.place(anchor = "c", relx = 0.5, rely = 0.3)
        frame22 = tk.Frame(frame2, width = 500, height = 200)
        frame22.place(anchor = "c", relx = 0.5, rely = 0.75)
        frame3 = tk.Frame(self.mainWindow, width = 500, height = 150) #, bg = 'blue')
        frame3.grid(row = 2, column = 1, sticky = 'news')
        frame31 = tk.Frame(frame3, width = 500, height = 150)
        frame31.place(anchor = "c", relx = 0.5, rely = 0.5)
        frame4 = tk.Frame(self.mainWindow, width = 200, height = 500) #, bg = 'green')
        frame4.grid(row = 0, rowspan = 3, column = 2, sticky = 'news')
        frame41 = tk.Frame(frame4, width = 200, height = 500)
        frame41.place(anchor = "c", relx = 0.5, rely = 0.5)
        
        # Logo
        imagePath = "assets/mazeGUIlogo.png"
        img = Image.open(imagePath)
        img = img.resize((420, 150))
        self.img = ImageTk.PhotoImage(master = frame21, width = 150, height = 150, image = img)
        logo = tk.Label(frame21, image = self.img)
        logo.place(anchor = "c", relx = 0.5, rely = 0.5)
            
        # Save data
        self.fileExtension = ".pickle "
        
        
        """
        Doors
        
        """
        
        # Maze state
        self.mazeState = 0
        tk.Label(frame11, font = buttonFont, text = "maze state", width = 12, anchor  = 'e').grid(row = 1, column = 0, padx = 10)
        self.mazeStateLabel = tk.Label(frame11, bg = self.backGroundColor, font = buttonFont, text = "idle", width = 8)
        self.mazeStateLabel.grid(row = 1, column = 1)
        self.mazeStateValue = tk.Label(frame11, font = buttonFont, text = self.mazeState)
        self.mazeStateValue.grid(row = 1, column = 2)
        
        # Door labels
        tk.Label(frame11, font = buttonFont, text = "Doors", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3 , padx = 10, pady = 10, sticky = 'we')
        labelList = ["start left", "start right", "decision left", "decision right"]
        nrow = 2
        for i in range(len(labelList)):
            tk.Label(frame11, font = buttonFont, text = labelList[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
            
        # Door states
        self.leftStartLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.leftStartLabel.grid(row = 2, column = 1)
        self.rightStartLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.rightStartLabel.grid(row = 3, column = 1)
        self.leftDecisionLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.leftDecisionLabel.grid(row = 4, column = 1)
        self.rightDecisionLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.rightDecisionLabel.grid(row = 5, column = 1)
        
        # IR sensor values
        self.leftStartValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.leftStartValue.grid(row = 2, column = 2)
        self.rightStartValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.rightStartValue.grid(row = 3, column = 2)
        self.leftDecisionValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.leftDecisionValue.grid(row = 4, column = 2)
        self.rightDecisionValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.rightDecisionValue.grid(row = 5, column = 2)
        
        
        """
        Task Parameters
        
        """
        
        # Parameters labels
        tk.Label(frame22, font = buttonFont, text = "Task Parameters", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 4 , padx = 10, pady = 10, sticky = 'we')
        entryLabels0 = ["trials", "duration", "task", "startDoor", "cues"]
        entryLabels2 = ["rig", "animal", "block", "path", "autoSave", " "]
        nrow = 1
        for i in range(len(entryLabels0)):
            tk.Label(frame22, font = buttonFont, text = entryLabels0[i], width = 8, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            tk.Label(frame22, font = buttonFont, text = entryLabels2[i], width = 8, anchor  = 'e').grid(row = nrow, column = 2, padx = 10)
            nrow += 1
        
        # Maximum number of trials entry
        self.maximumTrialNumber = 200
        self.trialsEntry = tk.Entry(frame22, font = 8, width = 14)
        self.trialsEntry.insert(0, self.maximumTrialNumber)
        self.trialsEntry.grid(row = 1, column = 1, sticky ='w')
        
        # Time limit entry
        self.timeout = 60 * 60 # in seconds
        self.timeEntry = tk.Entry(frame22, font = 8, width = 14)
        self.timeEntry.insert(0, self.timeout)
        self.timeEntry.grid(row = 2, column = 1, sticky ='w')
        
        # Task type list
        self.taskList = ["driftingGratings", "motionSelectivity", "whiteNoise", "objectDiscrimination", "valveCalibration"]
        self.taskName = " "
        self.taskBox = ttk.Combobox(frame22, width = 12, font = 8, state = 'readonly', values = self.taskList)
        self.taskBox.grid(row = 3, column = 1, sticky ='w')
        self.stimulusScreen = int(configurationData["stimulusScreen"]["screenNumber"])
        self.screenSize = (int(configurationData["stimulusScreen"]["screenWidth"]), int(configurationData["stimulusScreen"]["screenHeight"]))
        
        # Animal start list
        self.startList = ["left", "right"]   # 0 = left, 1 = right
        self.startBox = ttk.Combobox(frame22, width = 12, font = 8, state = 'readonly', values = self.startList)
        self.startBox.current(0)
        self.startBox.grid(row = 4, column = 1, sticky ='w')
        
        # Cues checkBox
        self.useTrialCues = tk.BooleanVar(value = True)
        self.cuesBox = tk.Checkbutton(frame22, text = "sounds + LEDs", font = 8, variable = self.useTrialCues, onvalue = True, offvalue = False)
        self.cuesBox.grid(row = 5, column = 1, sticky = 'w')

        # Sound for correct trials
        self.Fs = 44100
        correctFrequency = 5000
        correctTime = 1
        originalFs = 10000
        t = np.linspace(0, correctTime, correctTime * originalFs, False)
        correctSound = np.cos(2 * np.pi * correctFrequency * t)
        newT = np.linspace(0, correctTime, correctTime * self.Fs, False)
        correctSound = np.interp(newT,t,correctSound)
        correctSound = correctSound * (2**15 - 1) / np.max(np.abs(correctSound))
        self.correctSound = correctSound.astype(np.int16)
        
        # Sound for incorrect trials
        incorrectFrequency = 10000
        incorrectTime = 2
        originalFs = 10000
        t = np.linspace(0, incorrectTime, incorrectTime * originalFs, False)
        incorrectSound = np.cos(2 * np.pi * incorrectFrequency * t)
        noise = (2 * np.random.rand(len(incorrectSound))) - 1
        incorrectSound = incorrectSound + noise
        newT = np.linspace(0, incorrectTime, incorrectTime * self.Fs, False)
        incorrectSound = np.interp(newT,t,incorrectSound)
        incorrectSound = incorrectSound * (2**15 - 1) / np.max(np.abs(incorrectSound))
        self.incorrectSound = incorrectSound.astype(np.int16)
        
        # Rig ID entry
        self.rigID = "mazeRig"
        self.rigEntry = tk.Entry(frame22, font = 8, width = 14)
        self.rigEntry.insert(0, self.rigID)
        self.rigEntry.grid(row = 1, column = 3, sticky ='w')
        
        # Animal ID entry
        self.animalID = "J000_NC"
        self.animalEntry = tk.Entry(frame22, font = 8, width = 14)
        self.animalEntry.insert(0, self.animalID)
        self.animalEntry.grid(row = 2, column = 3, sticky = 'w')
        
        # Block ID entry
        self.blockID = "1"
        self.blockEntry = tk.Entry(frame22, font = 8, width = 14)
        self.blockEntry.insert(0, self.blockID)
        self.blockEntry.grid(row = 3, column = 3, sticky = 'w')
        
        # Path entry
        userName = os.getlogin()
        self.currentDate = datetime.today().strftime("%y%m%d")
        self.pathForSavingData = "C:\\Users\\" + userName + "\\Documents\\automatedMouseMaze\\Data\\" + self.currentDate + "\\"
        self.pathEntry = tk.Entry(frame22, font = 8, width = 14)
        self.pathEntry.insert(0, self.pathForSavingData)
        self.pathEntry.grid(row = 4, column = 3, sticky ='w')
        
        # Prepare directory to save data
        Path(self.pathForSavingData).mkdir(parents = True, exist_ok = True)
        
        # AutoSave checkBox
        self.autoSaveData = tk.BooleanVar(value = True)
        self.autoSaveBox = tk.Checkbutton(frame22, text = "save to path", font = 8, variable = self.autoSaveData, onvalue = True, offvalue = False)
        self.autoSaveBox.grid(row = 5, column = 3, sticky = 'w')
        
        
        """
        Behavior Stats
        
        """
        
        # Stats labels
        tk.Label(frame12, font = buttonFont, text = "Behavior", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3 , padx = 10, pady = 10, sticky = 'we')
        labelList = ["performance", "bias index", "trials", "correct", "incorrect", "left decisions", "right decisions", "reward (μL)"]
        nrow = 1
        for i in range(len(labelList)):
            tk.Label(frame12, font = buttonFont, text = labelList[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
            
        # Behavior parameters
        self.performance = 0
        self.biasIndex = 0
        self.trialID = 0
        self.correct = 0
        self.incorrect = 0
        self.left = 0
        self.right = 0
        
        # RNG for randomizing trials
        self.mazeRNG = np.random.default_rng(seed = None)
        
        # Reward
        self.estimatedReward = 0
        self.rewardStreak = [32, 36, 41, 45, 50, 54] # in ms
        self.rewardAmounts = [ 5,  6,  7,  8,  9, 10] # in μL
        
        # Behavior values in GUI
        self.performanceValue = tk.Label(frame12, font = buttonFont, text = self.performance)
        self.performanceValue.grid(row = 1, column = 1)
        self.biasIndexValue = tk.Label(frame12, font = buttonFont, text = self.biasIndex)
        self.biasIndexValue.grid(row = 2, column = 1)
        self.trialValue = tk.Label(frame12, font = buttonFont, text = self.trialID)
        self.trialValue.grid(row = 3, column = 1)
        self.correctValue = tk.Label(frame12, font = buttonFont, text = self.correct)
        self.correctValue.grid(row = 4, column = 1)
        self.incorrectValue = tk.Label(frame12, font = buttonFont, text = self.incorrect)
        self.incorrectValue.grid(row = 5, column = 1)
        self.leftValue = tk.Label(frame12, font = buttonFont, text = self.left)
        self.leftValue.grid(row = 6, column = 1)
        self.rightValue = tk.Label(frame12, font = buttonFont, text = self.right)
        self.rightValue.grid(row = 7, column = 1)
        self.rewardValue = tk.Label(frame12, font = buttonFont, text = self.estimatedReward)
        self.rewardValue.grid(row = 8, column = 1)
        
        
        """
        Task Control Buttons
        
        """
        
        # Ready button
        self.readyButton = tk.Button(frame31, text = 'Initialize Task', font = buttonFont, width = 12, command = self.readyTask)
        self.readyButton.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Cancel button
        self.cancelButton = tk.Button(frame31, text = 'Cancel Task', font = buttonFont, width = 12, command = self.cancelTask)
        self.cancelButton.grid(row = 1, column = 0,padx = 0, pady = 10)
        self.cancelButton.bind('<Enter>', lambda e: self.cancelButton.config(fg='Black', bg='#FFB844'))
        self.cancelButton.bind('<Leave>', lambda e: self.cancelButton.config(fg='Black', bg='SystemButtonFace'))
        
        # Start button
        self.startButton = tk.Button(frame31, text = 'Start Task', font = buttonFont, width = 12, command = self.runTask)
        self.startButton.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Black', bg ='#99D492'))
        self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # End task button
        self.endButton = tk.Button(frame31, text = 'End Task', font = buttonFont, width = 12, command = self.endTask)
        self.endButton.grid(row = 1, column = 1,padx = 10, pady = 10)
        self.endButton.bind('<Enter>', lambda e: self.endButton.config(fg='Black', bg='#DC5B5B'))
        self.endButton.bind('<Leave>', lambda e: self.endButton.config(fg='Black', bg='SystemButtonFace'))
        
        # Save button
        self.saveButton = tk.Button(frame31, text = 'Save Data', font = buttonFont, width = 12, command = self.saveData)
        self.saveButton.grid(row = 0, column = 2,padx = 10, pady = 10)
        self.saveButton.bind('<Enter>', lambda e: self.saveButton.config(fg='Black', bg='#84E0E0'))
        self.saveButton.bind('<Leave>', lambda e: self.saveButton.config(fg='Black', bg='SystemButtonFace'))
        
        # Close app button
        self.closeButton = tk.Button(frame31, text = 'Close', font = buttonFont, width = 12, command = self.closeMainWindow)
        self.closeButton.grid(row = 1, column = 2,padx = 0, pady = 10)
        self.closeButton.bind('<Enter>', lambda e: self.closeButton.config(fg='Black', bg='#AFAFAA'))
        self.closeButton.bind('<Leave>', lambda e: self.closeButton.config(fg='Black', bg='SystemButtonFace'))
        self.mainWindow.protocol('WM_DELETE_WINDOW', self.closeMainWindow)
        
        
        """
        Camera Controls
        
        """
        
        # Frame rate
        frameRate = 100                                  # (Hz). True frame rate must estimated. Delays caused by other computations in the code, and camera limitations
        self.cameraTimeBetweenFrames = 1000/frameRate    # miliseconds betweem frames
        
        # Booleans for buttons
        self.camerasAreOn = False
        self.saveVideo = False
        
        # Camera labels
        tk.Label(frame41, font = buttonFont, text = "Camera Controls", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 4 , padx = 10, pady = 10, sticky = 'we')
        
        # Initialize cameras
        self.startCameraButton = tk.Button(frame41, text = 'Start Cameras', font = buttonFont, width = 17, command = self.startCameras)
        self.startCameraButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))

        # Start recording
        self.recordCameraButton = tk.Button(frame41, text = 'Record Video', font = buttonFont, width = 17, command = self.recordVideo)
        self.recordCameraButton.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
        self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Stop recording
        self.stopRecordCameraButton = tk.Button(frame41, text = 'Stop Recording', font = buttonFont, width = 17, command = self.stopVideo)
        self.stopRecordCameraButton.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.stopRecordCameraButton.bind('<Enter>', lambda e: self.stopRecordCameraButton.config(fg = 'Black', bg ='#FFB844'))
        self.stopRecordCameraButton.bind('<Leave>', lambda e: self.stopRecordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))

        # Close cameras
        self.closeCameraButton = tk.Button(frame41, text = 'Close Cameras', font = buttonFont, width = 17, command = self.closeCameras)
        self.closeCameraButton.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.closeCameraButton.bind('<Enter>', lambda e: self.closeCameraButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.closeCameraButton.bind('<Leave>', lambda e: self.closeCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        
        """
        Teensy 4.0 pins
        
        """
        
        # Upload Firmata > StandardFirmata in Arduino IDE
        self.port = configurationData["teensyConfiguration"]["port"]
        self.boardName = "Teensy 4.0"
        
        # Door sensors
        self.leftStartIRsensor = int(configurationData["teensyConfiguration"]["leftStartIRsensor"])
        self.rightStartIRsensor = int(configurationData["teensyConfiguration"]["rightStartIRsensor"])
        self.leftDecisionIRsensor = int(configurationData["teensyConfiguration"]["leftDecisionIRsensor"])
        self.rightDecisionIRsensor = int(configurationData["teensyConfiguration"]["rightDecisionIRsensor"])
        
        # Door actuators
        self.leftStartDoor = int(configurationData["teensyConfiguration"]["leftStartDoor"])
        self.rightStartDoor = int(configurationData["teensyConfiguration"]["rightStartDoor"])
        self.leftDecisionDoor = int(configurationData["teensyConfiguration"]["leftDecisionDoor"])
        self.rightDecisionDoor = int(configurationData["teensyConfiguration"]["rightDecisionDoor"])
        
        # Water ports and LEDs
        self.leftWaterPort = int(configurationData["teensyConfiguration"]["leftWaterPort"])
        self.rightWaterPort = int(configurationData["teensyConfiguration"]["rightWaterPort"])
        self.leftLED = int(configurationData["teensyConfiguration"]["leftLED"])
        self.rightLED = int(configurationData["teensyConfiguration"]["rightLED"])
        
        # Check available serial ports
        availableSerialPorts = serial.tools.list_ports.comports()
        portIDs = []
        for port, desc, hwid in sorted(availableSerialPorts):
            portIDs.append(port[3])
        
        if not self.port[3] in portIDs:
            self.closeGUIWithoutCheckouts = True
            messagebox.showerror("Error", "Make sure the serial port for Teensy 4.0 in 'config/package.json' is correct before initializing maze.")
        else:
            self.closeGUIWithoutCheckouts = False
    
    """
    Teensy 4.0 Functions
    
    """
    
    def checkIfPortAvailable(self):
        
        try:
            s = serial.Serial(self.port)
            s.close()
            result = True
        except (OSError, serial.SerialException):
            result = False
            pass
        return result
    
    def connectToTeensy(self):
        
        # Check if Teensy 4.0 is available before attempting to connect
        boardAvailable = self.checkIfPortAvailable()
        
        # Connect to Teensy 4.0
        if boardAvailable is True:
            # Set up board layout
            print("Setting up the connection to",self.boardName,"...")
            self.board = pyfirmata.Arduino(self.port)
            teensyLayout = {
                            'digital': tuple(x for x in range(24)),
                            'analog': tuple(x for x in range(14, 24)),
                            'pwm': tuple(x for x in range(16)),
                            'use_ports': True,
                            'disabled': (0)
                                           }
            self.board.setup_layout(teensyLayout)
            it = pyfirmata.util.Iterator(self.board)
            it.start()
            # Set up pins
            self.board.get_pin('d:'+str(self.leftDecisionIRsensor)+':i')
            self.board.get_pin('d:'+str(self.rightDecisionIRsensor)+':i')
            self.board.get_pin('d:'+str(self.leftStartIRsensor)+':i')
            self.board.get_pin('d:'+str(self.rightStartIRsensor)+':i')
            self.board.get_pin('d:'+str(self.leftDecisionDoor)+':o')
            self.board.get_pin('d:'+str(self.rightDecisionDoor)+':o')
            self.board.get_pin('d:'+str(self.leftStartDoor)+':o')
            self.board.get_pin('d:'+str(self.rightStartDoor)+':o')
            self.board.get_pin('d:'+str(self.leftWaterPort)+':o')
            self.board.get_pin('d:'+str(self.rightWaterPort)+':o')
            self.board.get_pin('d:'+str(self.leftLED)+':o')
            self.board.get_pin('d:'+str(self.rightLED)+':o')
            print(self.boardName,"is now connected.")
        elif boardAvailable is False:
            print(self.boardName," is not avaiable...")
        return self.board
    
    def disconnectFromTeensy(self):
        
        # Check if Teensy 4.0 is 'not' available before attempting to disconnect
        boardAvailable = self.checkIfPortAvailable()
        
        # Disconnect from Teensy 4.0
        if boardAvailable is False:
            try:
                # Reset maze GUI and Doors
                doorNames = [self.leftStartDoor, self.rightStartDoor, self.leftDecisionDoor, self.rightDecisionDoor]
                for i in range(len(doorNames)):
                    self.board.digital[doorNames[i]].write(0)
                self.leftStartLabel.config(bg = '#99D492', text = "open")
                self.rightStartLabel.config(bg = '#99D492', text = "open")
                self.leftDecisionLabel.config(bg = '#99D492', text = "open")
                self.rightDecisionLabel.config(bg = '#99D492', text = "open")
                self.leftDecisionValue.config(text = 0)
                self.rightDecisionValue.config(text = 0)
                self.leftStartValue.config(text = 0)
                self.rightStartValue.config(text = 0)
                self.mazeStateLabel.config(bg = self.backGroundColor, text = "idle")
                self.mazeStateValue.config(text = 0)
                # Disconnect Teensy 4.0
                self.board.exit()
                print("Connection with",self.boardName,"is now closed...")
            except:
                print("Connection with",self.boardName,"has not been established yet.")
            else:
                s = serial.Serial(self.port)
                s.close()
        elif boardAvailable is True:
            print("Connection with",self.boardName,"has not been established yet.")
    
    
    """
    Doors, IR Sensors and Solenoid Valves
    
    """
    
    def updateDoors(self):
        
        # Before trial start
        if self.mazeState == 0:
            self.mazeStateLabel.config(bg = '#A9C6E3', text = "ready")
            self.mazeStateValue.config(text = 0)
            self.board.digital[self.leftStartDoor].write(1)
            self.board.digital[self.rightStartDoor].write(1)
            self.board.digital[self.leftDecisionDoor].write(1)
            self.board.digital[self.rightDecisionDoor].write(1)
            self.leftStartLabel.config(bg = 'pink', text = "closed")
            self.rightStartLabel.config(bg = 'pink', text = "closed")
            self.leftDecisionLabel.config(bg = 'pink', text = "closed")
            self.rightDecisionLabel.config(bg = 'pink', text = "closed")
            
        # Trial start
        if self.mazeState == 1:
            self.mazeStateLabel.config(bg = '#99D492', text = "start")
            self.mazeStateValue.config(text = 1)
            self.board.digital[self.leftStartDoor].write(1)
            self.board.digital[self.rightStartDoor].write(1)
            self.board.digital[self.leftDecisionDoor].write(0)
            self.board.digital[self.rightDecisionDoor].write(0)
            self.leftStartLabel.config(bg = 'pink', text = "closed")
            self.rightStartLabel.config(bg = 'pink', text = "closed")
            self.leftDecisionLabel.config(bg = '#99D492', text = "open")
            self.rightDecisionLabel.config(bg = '#99D492', text = "open")
            
        # After a decision has been recorded
        elif self.mazeState == 2:
            self.mazeStateLabel.config(bg = 'pink', text = "end")
            self.mazeStateValue.config(text = 2)
            self.board.digital[self.leftDecisionDoor].write(1)
            self.board.digital[self.rightDecisionDoor].write(1)
            self.leftDecisionLabel.config(bg = 'pink', text = "closed")
            self.rightDecisionLabel.config(bg = 'pink', text = "closed")
            
        # Mouse coming from the left
        elif self.mazeState == 3:
            self.mazeStateLabel.config(bg = '#A9C6E3', text = "ITI-left")
            self.mazeStateValue.config(text = 3)
            self.board.digital[self.leftStartDoor].write(0)
            self.leftStartLabel.config(bg = '#99D492', text = "open")
            
        # Mouse coming from the right
        elif self.mazeState == 4:
            self.mazeStateLabel.config(bg = '#A9C6E3', text = "ITI-right")
            self.mazeStateValue.config(text = 4)
            self.board.digital[self.rightStartDoor].write(0)
            self.rightStartLabel.config(bg = '#99D492', text = "open")
    
    def readPinStates(self):
        
        # Read pins
        self.LD = self.board.digital[self.leftDecisionIRsensor].read()
        self.RD = self.board.digital[self.rightDecisionIRsensor].read()
        self.LS = self.board.digital[self.leftStartIRsensor].read()
        self.RS = self.board.digital[self.rightStartIRsensor].read()
        
        # Update door values in GUI
        doorLabelValues = [self.leftStartValue, self.rightStartValue, self.leftDecisionValue, self.rightDecisionValue]
        pinStates = [self.LS,self.RS,self.LD,self.RD]
        for i in range(len(doorLabelValues)):
            if pinStates[i] is False:
                doorLabelValues[i].config(text = 0)
            elif self.LD is True or self.RD is True:
                doorLabelValues[i].config(text = 1)
            doorLabelValues[i].update_idletasks()
            
    def updateMazeState(self):
        
        # Maze state
        currentMazeState = self.mazeState
        
        # Update maze states
        if self.mazeState == 1:
            if self.LD is False or self.RD is False:
                self.mazeState = 2
                self.endTrial()
                self.interTrialStart = time.time()
                if self.LD is False:
                    self.startDoor = "left"
                elif self.RD is False:
                    self.startDoor = "right"
        elif self.mazeState == 2:
            self.closeValve()
            if self.reward == False and self.initializeTrial == True:
                self.initializeUpcomingTrial()
                self.initializeTrial = False
            currentTime = time.time()
            if currentTime > self.interTrialStart + self.interTrialTimeOut:
                if self.startDoor == "left":
                    self.mazeState = 3
                elif self.startDoor == "right":
                    self.mazeState = 4
                self.initializeTrial = True
        elif self.mazeState == 3:
            if self.LS is False:
                self.mazeState = 1
                self.startTrial()
        elif self.mazeState == 4:
            if self.RS is False:
                self.mazeState = 1
                self.startTrial()
                
        # Update doors
        if currentMazeState != self.mazeState:
            self.updateDoors()

    def closeValve(self):
        
        if self.reward is True:
            currentTime =  time.time()
            if currentTime > self.rewardStart + self.rewardTime:
                self.board.digital[self.waterPort].write(0)
                self.board.digital[self.LED].write(0)
                self.reward = False

    def giveReward(self):
        
        if self.reward is False:
            if self.targetLocation == 0:
                self.waterPort = self.leftWaterPort
                self.LED = self.leftLED
            elif self.targetLocation == 1:
                self.waterPort = self.rightWaterPort
                self.LED = self.rightLED
            self.reward = True
            self.estimatedReward = self.estimatedReward + self.rewardSize
            self.board.digital[self.waterPort].write(1)
            self.board.digital[self.LED].write(1)
            self.rewardStart = time.time()


    """ 
    Camera Functions
    
    """

    def startCameras(self):
        
        if self.camerasAreOn == False:
        
            # Check for task parameters
            self.updateTrialParameters()
        
            # Update startCameraButton: starting cameras...
            self.startCameraButton.config(fg = 'Black', bg = '#A9C6E3', text = 'Starting...', relief = 'sunken')
            self.startCameraButton.update_idletasks()
    
            # Create window
            self.cameraWindow = tk.Toplevel()
            self.cameraWindow.title("Cameras")
            
            # Initialize camera objects
            self.eyeCamera = cv2.VideoCapture(0) 
            self.worldCamera = cv2.VideoCapture(1) 
            self.cameraTimeStamps = []
            self.eyeCamRet = None
            self.worldCamRet = None
            self.eyeCamFrame = None
            self.worldCamFrame = None
            self.camerasAreOn = True
            self.okToSaveVideoFiles = False
            self.saveVideo = False
            self.noVideoRecorded = True
       
            # Check if cameras are already open
            if (self.eyeCamera.isOpened() == False):  
                print("Error reading eye camera") 
            if (self.worldCamera.isOpened() == False):  
                print("Error reading world camera") 
              
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
                self.okToSaveVideoFiles = messagebox.askyesno("Existing file", "Do you want to overwrite video files?")
            
            # Video files
            if self.okToSaveVideoFiles == True:
                self.eyeCameraVideo = cv2.VideoWriter(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "eyeCamera" + "_" + str(self.blockID) + ".avi",
                                                      cv2.VideoWriter_fourcc(*'MJPG'), 10, eyeCamSize)
                self.worldCameraVideo = cv2.VideoWriter(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "worldCamera" + "_" + str(self.blockID) + ".avi",
                                                        cv2.VideoWriter_fourcc(*'MJPG'), 10, worldCamSize)
                videoFilesReady = True
            else:
                videoFilesReady = False
                self.camerasAreOn = False
    
            if videoFilesReady == True:
                
                # Update startCameraButton: cameras are open (preview mode)...
                self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Preview')
                self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Blue', bg ='#A9C6E3'))
                self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3'))
                self.startCameraButton.update_idletasks()
                
                # Start cameras
                self.cameraThread = Thread(target = self.updateCameras)
                self.cameraThread.start()
                
                # Camera window
                self.cameraWindow.protocol('WM_DELETE_WINDOW', self.closeCameras)
                self.cameraWindow.mainloop()
                
            elif videoFilesReady == False:
                
                # Reset startCameraButton
                self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
                self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
                self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
                self.startCameraButton.update_idletasks()
                
                # Destroy camera window
                self.resetCameras()
                
                # Warning: change block number
                messagebox.showwarning("Video recording", "Please choose a different block number for you experiment." +
                                                          "\n" +
                                                          "\nCurrent block number already exists.")
            
        else:
            
            print("Cameras are already on.")
        
    def recordVideo(self):
        
        if self.camerasAreOn == True:
            
            # Update camera buttons. Recording video...
            self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
            self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.startCameraButton.update_idletasks()
            self.recordCameraButton.config(fg = 'Black', bg = '#DC5B5B', relief = 'sunken', text = 'Recording')
            self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
            self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg = '#DC5B5B'))
            self.recordCameraButton.update_idletasks()
            
            # Turning saving frames on
            self.saveVideo = True
            self.noVideoRecorded = False
            
        else:
            
            messagebox.showinfo("Cameras", "Cameras have not been started yet.", parent = self.mainWindow)
        
    def stopVideo(self):
        
        if self.saveVideo == True:
        
            # Update recordCameraButton: stop video recording...
            self.recordCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Record Video')
            self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg = 'SystemButtonFace'))
            self.recordCameraButton.update_idletasks()
            
            # Turning saving frames off
            self.saveVideo = False
            
        else:
            
            print("There is no ongoing video recording...")
        
    def updateCameras(self):
        
        if self.camerasAreOn == True:
        
                # Grab frame
                self.eyeCamRet, self.eyeCamFrame = self.eyeCamera.read()
                self.worldCamRet, self.worldCamFrame = self.worldCamera.read()
                self.cameraTimeStamps.append(time.time())
                self.worldCamFrame = cv2.rotate(self.worldCamFrame, cv2.ROTATE_180)
                
                if self.eyeCamRet == True or self.worldCamRet == True:
                    
                    # Save frame to video file
                    if self.saveVideo == True:
                        self.eyeCameraVideo.write(self.eyeCamFrame)
                        self.worldCameraVideo.write(self.worldCamFrame)
                    
                    # Update frame to display
                    self.combinedFrame = cv2.vconcat([self.worldCamFrame, self.eyeCamFrame])
                    self.combinedFrame = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(self.combinedFrame, cv2.COLOR_BGR2RGB)))
                    self.canvas.itemconfig(self.canvasImage, image = self.combinedFrame)
                    
                # Loop
                self.cameraWindow.after(int(self.cameraTimeBetweenFrames), self.updateCameras)
        
    def closeCameras(self):
        
        if self.camerasAreOn == True:
            
            # Reset camera buttons
            self.startCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start Cameras')
            self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.startCameraButton.update_idletasks()
            self.recordCameraButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Record Video')
            self.recordCameraButton.bind('<Enter>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='#DC5B5B'))
            self.recordCameraButton.bind('<Leave>', lambda e: self.recordCameraButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.recordCameraButton.update_idletasks()
            
            # Stop grabing frames and close window
            self.camerasAreOn = False
            self.saveVideo = False
            self.cameraWindow.after(50, self.resetCameras)
            
        else:
            
            print("Cameras are currently closed.")
        
    def resetCameras(self):
        
        # Stop camera objects
        self.eyeCamera.release() 
        self.worldCamera.release()
        
        # Stop video files
        if self.okToSaveVideoFiles == True:
            
            # Close video files
            self.eyeCameraVideo.release() 
            self.worldCameraVideo.release()
            
            # If frames were not recorded, destroy video files
            if self.noVideoRecorded == True:
                os.remove(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "eyeCamera" + "_" + str(self.blockID) + ".avi")
                os.remove(self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "worldCamera" + "_" + str(self.blockID) + ".avi")
                
            # If frames were recorded, save time stamps
            if self.noVideoRecorded == False:
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
    Task Functions
    
    """
    
    def initializeTaskParameters(self):
        
        # Task
        self.runningTask = False
        self.initializeTrial = True
        self.interTrialStart = 0
        self.interTrialTimeOut = 0
        self.correctInterTrialTimeOut = 3
        self.incorrectInterTrialTimeOut = 10
        self.probabilityTargetLeft = 0.5
        
        # Behavior stats
        self.performance = 0
        self.biasIndex = 0
        self.trialID = 0
        self.correct = 0
        self.incorrect = 0
        self.left = 0
        self.right = 0
        self.trialType = 0
        self.lastDecision = []
        
        # Recent behavior
        self.recentBiasIndex = 0
        self.recentPerformance = 0
        
        # Reward
        self.reward = False
        self.estimatedReward = 0
        self.correctStreak = 0
        
        # Experiment data
        self.dataFrameTrial = []
        self.dataFrameTarget = []
        self.dataFrameDecision = []
        self.dataFrameCorrect = []
        self.dataFrameTrialType = []
        self.dataFrameStartDoor = []
        self.dataFrameLeftProbability = []
        self.dataFrameStartTime = []
        self.dataFrameEndTime = []
        self.dataFrameRawTaskStartTime = []
    
        # Update behavior stats in GUI
        self.updateBehaviorStats()
    
    def updateTrialParameters(self):
        
        # Input task parameters
        self.maximumTrialNumber = int(self.trialsEntry.get())
        self.timeout = int(self.timeEntry.get())
        self.taskName = str(self.taskBox.get())
        self.startDoor = str(self.startBox.get())
        self.trialCues = bool(self.useTrialCues.get())
        self.animalID = str(self.animalEntry.get())
        self.rigID = str(self.rigEntry.get())
        self.blockID = str(self.blockEntry.get())
        self.autoSave = bool(self.autoSaveData.get())
        
    def readyTask(self):
        
        # Check if Teensy 4.0 is available before attempting to initialize a task
        boardAvailable = self.checkIfPortAvailable()
        
        if boardAvailable is True:
        
            # Update task parameters
            self.updateTrialParameters()
            
            # Flush all data from previous task
            self.initializeTaskParameters()
            
            # Display task parameters when initializing task
            print(" ")
            if not self.taskName == "valveCalibration":
                print("     Task Parameters:")
                print("          Task name:",self.taskName)
                print("          Maximum number of trials:",self.maximumTrialNumber)
                print("          Maximum session time (s):",self.timeout)
                print("          Start door:",self.startDoor)
                print("          Use sound cues:",str(self.trialCues).lower())
                print("          Animal ID:",self.animalID)
                print("          Rig ID:",self.rigID)
                print("          Block ID:",self.blockID)
                print("          AutoSave:",self.autoSave)
            else:
                print("     Valve Calibration:")
                print("          Try different opening time windows to build your calibration curve.")
                print("          Example:")
                print("               Time:           5,  10,  15,  20,  25,  30,  40,  50,  60,  80, 100")
                print("               Frequency:     25,  25,  20,  15,  15,  15,  10,  10,   5,   5,   5")
                print("               Repetitions: 1500, 750, 500, 400, 300, 250, 200, 150, 125, 100,  50")
            print(" ")
            
            # Initialize connection with Teensy 4.0
            if not self.taskName in self.taskList:
                messagebox.showerror("Error", "Please select a task before initializing maze.")
            else:
                # Update readyButton: connecting to board...
                self.readyButton.config(fg = 'Black', bg = '#A9C6E3', text = 'Connecting...', relief = 'sunken')
                self.readyButton.update_idletasks()
                # Connect to board
                self.connectToTeensy()
                # Update readyButton: task is ready...
                self.readyButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Ready')
                self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Blue', bg ='#A9C6E3'))
                self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Blue', bg = '#A9C6E3'))
                self.readyButton.update_idletasks()
                if not self.taskName == "valveCalibration":
                    # Update maze
                    self. mazeState = 0
                    self.updateDoors()
                
            # Initialize visual stimulus
            if self.taskName == "driftingGratings":
                self.visualStimulus = driftingGratings.driftingGratings(self.stimulusScreen, self.screenSize)
            elif self.taskName == "motionSelectivity":
                self.visualStimulus = motionSelectivity.motionSelectivity(self.stimulusScreen, self.screenSize)
            elif self.taskName == "whiteNoise":
                self.visualStimulus = whiteNoise.whiteNoise(self.stimulusScreen, self.screenSize)
            elif self.taskName == "objectDiscrimination":
                self.visualStimulus = objectDiscrimination.objectDiscrimination(self.stimulusScreen, self.screenSize)
            elif self.taskName == "valveCalibration":
                self.calibrationWindow = tk.Toplevel()
                waterPorts = [self.leftWaterPort, self.rightWaterPort]
                valveCalibration.valveCalibration(self.calibrationWindow, self.board, waterPorts)
                self.calibrationWindow.protocol('WM_DELETE_WINDOW', self.resetTask)
                self.calibrationWindow.mainloop()
                
            # Prepare upcoming stimulus
            if self.taskName in self.taskList and not self.taskName == "valveCalibration":
                
                # Disable task parameter boxes
                entryBoxes = [self.trialsEntry, self.timeEntry, self.taskBox, self.startBox, self.cuesBox, self.animalEntry, self.rigEntry, self.blockEntry, self.pathEntry, self.autoSaveBox]
                for i in range(len(entryBoxes)):
                    entryBoxes[i].config(state = 'disabled')
                    entryBoxes[i].update_idletasks()
                    
                # Prepare first trial
                self.initializeUpcomingTrial()
                
        else:
            
            if self.runningTask == True:
                
                print("Failed to initialize a task. There might be an ongoing task currently running...")
                
            else:
                
                print("Task has been already initialized. Waiting to start...")
            
    def cancelTask(self):
        
        boardAvailable = self.checkIfPortAvailable()
        if boardAvailable is False:
            if self.runningTask is True:
                print("Task is currently running. Cancelling task initialization is no longer available.")
            elif self.runningTask is False:
                self.resetTask()
                print("Task initialization has been cancelled.")
        elif boardAvailable is True:
            print("No task has been initialized yet.")
            
    def resetTask(self):
        
        # Disconnect Teensy 4.0
        boardAvailable = self.checkIfPortAvailable()
        if boardAvailable is False:
            # Reset maze
            self.board.digital[self.leftStartDoor].write(0)
            self.board.digital[self.rightStartDoor].write(0)
            self.board.digital[self.leftDecisionDoor].write(0)
            self.board.digital[self.rightDecisionDoor].write(0)
            self.board.digital[self.leftWaterPort].write(0)
            self.board.digital[self.rightWaterPort].write(0)
            self.board.digital[self.leftLED].write(0)
            self.board.digital[self.rightLED].write(0)
            # Disconnect Teensy board
            self.disconnectFromTeensy()
            # Reset GUI buttons
            self.startButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start')
            self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Black', bg ='#99D492'))
            self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.startButton.update_idletasks()
            self.readyButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Initialize')
            self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.readyButton.update_idletasks()
        
        # Reactivate task parameter boxes
        entryBoxes = [self.trialsEntry, self.timeEntry, self.taskBox, self.startBox, self.cuesBox, self.animalEntry, self.rigEntry, self.blockEntry, self.pathEntry, self.autoSaveBox]
        for i in range(len(entryBoxes)):
            entryBoxes[i].config(state = 'normal')
            entryBoxes[i].update_idletasks()
        
        # Save task data
        if not self.taskName == "valveCalibration":
            # Save experiment data
            if self.autoSave is True:
                self.saveData()
            # Close visual stimulus window
            self.visualStimulus.closeWindow()
        else:
            self.calibrationWindow.destroy()
            
    def initializeUpcomingTrial(self):
        
        # Target for upcoming trial
        self.targetLocation = self.mazeRNG.choice([0,1], p = [self.probabilityTargetLeft, 1-self.probabilityTargetLeft])
        
        # Upcoming viual stimulus
        self.visualStimulus.initializeStimulus(target = self.targetLocation)
        
        # Reward for upcoming trial
        if self.correctStreak < len(self.rewardStreak):
            self.rewardTime = self.rewardStreak[self.correctStreak] / 1000 # in s
            self.rewardSize = self.rewardAmounts[self.correctStreak] # in μL
        else:
            self.rewardTime = self.rewardStreak[-1] / 1000 # in s
            self.rewardSize = self.rewardAmounts[-1] # in μL
            
    def startTrial(self):
        
        # Display visual stimulus
        self.visualStimulus.startStimulus(display = True)
        
        # Display trial info in terminal
        self.trialID += 1
        print("     Trial ", self.trialID," started...", " Target -> ", self.targetLocation)
        
        # Append experiment data to data frame
        self.dataFrameTrial.append(self.trialID)
        self.dataFrameTarget.append(self.targetLocation)
        if self.startDoor == "left":
            self.dataFrameStartDoor.append(0)
        elif self.startDoor == "right":
            self.dataFrameStartDoor.append(1)
        self.dataFrameStartTime.append(time.time() - self.taskTimeStart)
            
    def endTrial(self):
        
        # Trial outcome
        self.triggerTrialOutcome()
        
        # End visual stimulus
        self.visualStimulus.stopStimulus(display = False)
        
        # Append experiment data to data frame
        self.dataFrameDecision.append(self.lastDecision)
        self.dataFrameTrialType.append(self.trialType)
        self.dataFrameEndTime.append(time.time() - self.taskTimeStart)
        if self.trialType == 1 or self.trialType == 4:
            self.dataFrameCorrect.append(1)
        elif self.trialType == 2 or self.trialType == 3:
            self.dataFrameCorrect.append(0)
        self.dataFrameLeftProbability.append(self.probabilityTargetLeft)
        
        # Bias correction and recent quick stats
        if self.trialID >= 10:
            recentDecisions = self.dataFrameDecision[-10:]
            self.recentBiasIndex = (recentDecisions.count(0) - recentDecisions.count(1)) / len(recentDecisions)
            self.probabilityTargetLeft = 0.5 - (self.recentBiasIndex/2)
            recentCorrect = self.dataFrameCorrect[-10:]
            self.recentPerformance = recentCorrect.count(1) / len(recentCorrect)
        
        # Display stats on terminal
        if self.trialType == 1:
            print("          >>> Correct Left <<<")
        elif self.trialType == 2:
            print("          --- Incorrect Left ---")
        elif self.trialType == 3:
            print("          --- Incorrect Right ---")
        elif self.trialType == 4:
            print("          >>> Correct Right <<<")
        if self.trialID <= 10:
            print("              Performance = ", self.performance)
            print("              Bias index = ", self.biasIndex)
        else:
            print("              Performance (recent)", self.recentPerformance, "     Performance (overall) = ", self.performance)
            print("              Bias index (recent) = ", self.recentBiasIndex,"     Bias index (overall) = ", self.biasIndex)
        
        # Update behavior stats in GUI
        self.updateBehaviorStats()
        
        # End task after last trial
        if self.trialID == self.maximumTrialNumber:
            self.runningTask = False
            print(" ")
            print("The task has reached the maximum number of trials!")
        
    def updateBehaviorStats(self):
        
        # Update behavior stats in GUI
        behaviorStats = [self.performance, self.biasIndex, self.trialID, self.correct, self.incorrect, self.left,self.right, self.estimatedReward]
        behaviorValues = [self.performanceValue, self.biasIndexValue, self.trialValue, self.correctValue, self.incorrectValue, self.leftValue, self.rightValue, self.rewardValue]
        for i in range(len(behaviorValues)):
            behaviorValues[i].config(text = behaviorStats[i])
            behaviorValues[i].update_idletasks()
        
        
    def triggerTrialOutcome(self):
        
        # Trial type and outcome
        if self.LD is False:
            self.left += 1
            if self.targetLocation == 0:
                self.correct += 1
                # Correct left
                self.giveReward()
                if self.trialCues is True:
                    sa.play_buffer(self.correctSound, 1, 2, self.Fs)
                self.interTrialTimeOut = self.correctInterTrialTimeOut
                self.trialType = 1
                self.lastDecision = 0
                self.correctStreak += 1
            elif self.targetLocation == 1:
                self.incorrect += 1
                # Incorrect left
                if self.trialCues is True:
                    sa.play_buffer(self.incorrectSound, 1, 2, self.Fs)
                self.interTrialTimeOut = self.incorrectInterTrialTimeOut
                self.trialType = 2
                self.lastDecision = 0
                self.correctStreak = 0
        elif self.RD is False:
            self.right += 1
            if self.targetLocation == 0:
                self.incorrect += 1
                # Incorrect right
                if self.trialCues is True:
                    sa.play_buffer(self.incorrectSound, 1, 2, self.Fs)
                self.interTrialTimeOut = self.incorrectInterTrialTimeOut
                self.trialType = 3
                self.lastDecision = 1
                self.correctStreak = 0
            elif self.targetLocation == 1:
                self.correct += 1
                # Correct right
                self.giveReward()
                if self.trialCues is True:
                    sa.play_buffer(self.correctSound, 1, 2, self.Fs)
                self.interTrialTimeOut = self.correctInterTrialTimeOut
                self.trialType = 4
                self.lastDecision = 1
                self.correctStreak += 1
                    
        # Quick stats
        self.performance = round(self.correct / (self.correct + self.incorrect),2)
        self.biasIndex = round((self.left-self.right) / (self.left+self.right),2)
        
    def runTask(self):
        
        if self.runningTask == False:
        
            # Update startButton: task is running...
            self.startButton.config(fg = 'Blue', bg = '#99D492', relief = 'sunken', text = 'Running...')
            self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Blue', bg ='#99D492'))
            self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Blue', bg = '#99D492'))
            self.startButton.update_idletasks()
            self.readyButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Initialize')
            self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.readyButton.update_idletasks()
            
            # Set up task
            if self.startDoor == "left":
                self.mazeState = 3
            elif self.startDoor == "right":
                self.mazeState = 4
            self.updateDoors()
            self.runningTask = True
            self.taskTimeStart = time.time()
            self.dataFrameRawTaskStartTime.append(self.taskTimeStart)
            print(" ")
            
            # Start task
            self.currentRunningTask = Thread(target = self.checkTask())
            self.currentRunningTask.start()
            self.resetTask()
            
        else:
            
            print("There is an ongoing task currently running...")
    
    def checkTask(self):
        
        # Check IR sensors and update task states
        while self.runningTask is True:
            self.mainWindow.update()
            self.readPinStates()
            self.updateMazeState()
            self.visualStimulus.updateStimulus()
            currentTime =  time.time()
            if currentTime > self.taskTimeStart + self.timeout:
                self.runningTask = False
                print(" ")
                print("The task has reached its time limit!")
            if self.runningTask is False:
                break
            
    def endTask(self):
        
        # Kill Thread loop
        if self.runningTask is True:
            print(" ")
            print("Task ended by user...")
            self.runningTask = False
        elif self.runningTask is False:
            print("There is no current task running at the moment.")
        
    def saveData(self):
        
        # Build dataFrame
        data = {
                "trial": self.dataFrameTrial,
                "startDoor": self.dataFrameStartDoor,
                "targetLeftProbability": self.dataFrameLeftProbability,
                "target": self.dataFrameTarget,
                "decision": self.dataFrameDecision,
                "correct": self.dataFrameCorrect,
                "trialType": self.dataFrameTrialType,
                "startTime": self.dataFrameStartTime,
                "endTime": self.dataFrameEndTime,
                "rawTaskStartTime": self.dataFrameRawTaskStartTime,
                                                                   }
        df = pd.DataFrame.from_dict(data, orient = 'index')
        df = df.transpose()
        
        # Save experiment data
        fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "behavior" + "_" + str(self.blockID)
        if df.empty:
            print("DataFrame is empty. Most likely an experiment has not been run yet.")
        else:
            if not os.path.isfile(fileName + self.fileExtension):
                df.to_pickle(fileName + self.fileExtension)
                messagebox.showinfo("Data Saved", "Experiment data have been saved at " + self.pathForSavingData)
            else:
                isNotSaved = True
                while isNotSaved is True:
                    blockID = fileName[-1]
                    blockID = int(blockID)
                    blockID += 1
                    fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "behavior" + "_" + str(blockID)
                    if not os.path.isfile(fileName + self.fileExtension):
                        df.to_pickle(fileName + self.fileExtension)
                        messagebox.showwarning("Data Saved", "Experiment data have been saved at " + self.pathForSavingData +
                                               "\n " +
                                               "\nHowever, the block number was changed to " + str(blockID) + " to avoid overwriting existing file." +
                                               "\n"
                                               "\nIf video was recorded, make sure block numbers match.")
                        isNotSaved = False
            print("Experiment data have been saved successfully.")
            print(" ")
       
    def closeMainWindow(self):
        
        # Kill GUI
        boardAvailable = self.checkIfPortAvailable()
        if boardAvailable is False and self.closeGUIWithoutCheckouts is False:
            print("Please click on 'End Task' before closing this program.")
        elif boardAvailable is True or self.closeGUIWithoutCheckouts is True:
            self.mainWindow.destroy()
            self.mainWindow.quit()