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

# Connectivity
import socket
import select

# Crown cameras
import crownCameras

# Open Ephys
import openEphys

# Teensy modules
import pyfirmata
import serial
import serial.tools.list_ports
import simpleaudio as sa

# Visual stimulus
import driftingGratings
import motionSelectivity
import whiteNoise
import objectDiscrimination

# Valve calibration
import valveCalibration

# Data modules
import time
import ntplib
import pickle
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
        
        # Geometry and location
        self.mainWindow = mainWindow
        self.mainWindow.title('Automated Mouse Maze')
        windowWidth = 1000
        windowHeight = 700
        screenWidth = self.mainWindow.winfo_screenwidth()
        screenHeight = self.mainWindow.winfo_screenheight()
        x = (screenWidth/1.5) - (windowWidth/2)
        y = (screenHeight/2) - (windowHeight/2)
        self.mainWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.backGroundColor = self.mainWindow.cget('bg')
        buttonFont = tkFont.Font(family = 'helvetica', size = 12)
        
        # Frame 1: Maze states and mouse behavior
        frame1 = tk.Frame(self.mainWindow, width = 225, height = 700)
        frame1.grid(row = 0, rowspan = 3, column = 0, sticky = 'news')
        frame11 = tk.Frame(frame1, width = 225, height = 235)
        frame11.place(anchor = "c", relx = 0.5, rely = 0.15)
        frame12 = tk.Frame(frame1, width = 225, height = 130)
        frame12.place(anchor = "c", relx = 0.5, rely = 0.415)
        frame13 = tk.Frame(frame1, width = 225, height = 335)
        frame13.place(anchor = "c", relx = 0.5, rely = 0.75)
        
        # Frame 2: Logo and main task settings
        frame2 = tk.Frame(self.mainWindow, width = 550, height = 550)
        frame2.grid(row = 0, rowspan = 2, column = 1, sticky = 'news')
        frame21 = tk.Frame(frame2, width = 550, height = 175)
        frame21.place(anchor = "c", relx = 0.5, rely = 0.215)
        frame22 = tk.Frame(frame2, width = 550, height = 375)
        frame22.place(anchor = "c", relx = 0.5, rely = 0.71)
        
        # Frame 3: Task buttons
        frame3 = tk.Frame(self.mainWindow, width = 550, height = 150)
        frame3.grid(row = 2, column = 1, sticky = 'news')
        frame31 = tk.Frame(frame3, width = 550, height = 150)
        frame31.place(anchor = "c", relx = 0.5, rely = 0.5)
        
        # Frame 4: Camera and Open Ephys controls
        frame4 = tk.Frame(self.mainWindow, width = 225, height = 700)
        frame4.grid(row = 0, rowspan = 3, column = 2, sticky = 'news')
        frame41 = tk.Frame(frame4, width = 225, height = 325)
        frame41.place(anchor = "c", relx = 0.5, rely = 0.225)
        frame42 = tk.Frame(frame4, width = 225, height = 375)
        frame42.place(anchor = "c", relx = 0.5, rely = 0.725)
        
        # Logo
        imagePath = "assets/mazeGUIlogo.png"
        img = Image.open(imagePath)
        img = img.resize((490, 175))
        self.img = ImageTk.PhotoImage(master = frame21, width = 490, height = 175, image = img)
        logo = tk.Label(frame21, image = self.img)
        logo.place(anchor = "c", relx = 0.5, rely = 0.5)
            
        # Save data
        self.fileExtension = ".pickle "
        
        
        """
        Doors
        
        """
        
        # Maze state
        self.mazeState = 0
        self.currentMazeState = 0
        tk.Label(frame11, font = buttonFont, text = "maze state", width = 12, anchor  = 'e').grid(row = 1, column = 0, padx = 10)
        self.mazeStateLabel = tk.Label(frame11, bg = self.backGroundColor, font = buttonFont, text = "idle", width = 8)
        self.mazeStateLabel.grid(row = 1, column = 1)
        self.mazeStateValue = tk.Label(frame11, font = buttonFont, text = self.mazeState)
        self.mazeStateValue.grid(row = 1, column = 2)
        
        # Door labels
        tk.Label(frame11, font = buttonFont, text = "Doors", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'we')
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

        # Current pin values
        self.LS = 0
        self.RS = 0
        self.LD = 0
        self.RD = 0
        self.stimulusOn = 0
        self.stimulusOff = 0
        
        
        """
        Visual Stimulus
        
        """
        
        # Stimulus state
        self.stimulusState = 0
        self.currentStimulusState = 0
        tk.Label(frame12, font = buttonFont, text = "stimulus state", width = 12, anchor  = 'e').grid(row = 1, column = 0, padx = 10)
        self.stimulusStateLabel = tk.Label(frame12, bg = self.backGroundColor, font = buttonFont, text = "idle", width = 8)
        self.stimulusStateLabel.grid(row = 1, column = 1)
        self.stimulusStateValue = tk.Label(frame12, font = buttonFont, text = self.stimulusState)
        self.stimulusStateValue.grid(row = 1, column = 2)
        
        # Stimulus labels
        tk.Label(frame12, font = buttonFont, text = "Stimulus", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'we')
        labelList = ["on switch", "off switch"]
        nrow = 2
        for i in range(len(labelList)):
            tk.Label(frame12, font = buttonFont, text = labelList[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
        
        # Stimulus states
        self.startStimulusLabel = tk.Label(frame12, bg = self.backGroundColor, font = buttonFont, text = "idle", width = 8)
        self.startStimulusLabel.grid(row = 2, column = 1)
        self.stopStimulusLabel = tk.Label(frame12, bg = self.backGroundColor, font = buttonFont, text = "idle", width = 8)
        self.stopStimulusLabel.grid(row = 3, column = 1)
        
        # IR sensor values
        self.startStimulusValue = tk.Label(frame12, font = buttonFont, text = 0)
        self.startStimulusValue.grid(row = 2, column = 2)
        self.stopStimulusValue = tk.Label(frame12, font = buttonFont, text = 0)
        self.stopStimulusValue.grid(row = 3, column = 2)
        
        
        """
        Task Settings
        
        """
        
        # Settings labels
        self.taskSettingsLabel = tk.Label(frame22, font = buttonFont, text = "Task Settings", width = 12, anchor  = 'c')
        self.taskSettingsLabel.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'we')
        self.experimentDataLabel = tk.Label(frame22, font = buttonFont, text = "Experiment Data", width = 12, anchor  = 'c')
        self.experimentDataLabel.grid(row = 0, column = 2, columnspan = 2, padx = 10, pady = 10, sticky = 'we')
        entryLabels0 = ["trials", "duration", "task", "start door", "cues", "stimulus", "stimulus", "forced choice"]
        entryLabels2 = ["rig", "animal", "block", "path", "auto save", " ", " ", " "]
        nrow = 1
        for i in range(len(entryLabels0)):
            tk.Label(frame22, font = buttonFont, text = entryLabels0[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            tk.Label(frame22, font = buttonFont, text = entryLabels2[i], width = 10, anchor  = 'e').grid(row = nrow, column = 2, padx = 10)
            nrow += 1
        tk.Label(frame22, font = buttonFont, text = "Acquisition Panel", width = 12, anchor  = 'c').grid(row = 6, column = 2, columnspan = 2, padx = 10, pady = 10, sticky = 'we')
        
        # Maximum number of trials entry
        self.maximumTrialNumber = 200
        self.trialsEntry = tk.Entry(frame22, font = 8, width = 14)
        self.trialsEntry.insert(0, self.maximumTrialNumber)
        self.trialsEntry.grid(row = 1, column = 1, sticky = 'w')
        
        # Time limit entry
        self.timeout = 60 * 60 # in seconds
        self.timeEntry = tk.Entry(frame22, font = 8, width = 14)
        self.timeEntry.insert(0, self.timeout)
        self.timeEntry.grid(row = 2, column = 1, sticky = 'w')
        
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
        self.startBox.grid(row = 4, column = 1, sticky = 'w')
        
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
        
        # Start stimulus checkBox
        self.startStimulusTrigger = tk.BooleanVar(value = True)
        self.startStimulusBox = tk.Checkbutton(frame22, text = "on switch", font = 8, variable = self.startStimulusTrigger, onvalue = True, offvalue = False)
        self.startStimulusBox.grid(row = 6, column = 1, sticky = 'w')
        
        # Stop stimulus checkBox
        self.stopStimulusTrigger = tk.BooleanVar(value = False)
        self.stopStimulusBox = tk.Checkbutton(frame22, text = "off switch", font = 8, variable = self.stopStimulusTrigger, onvalue = True, offvalue = False)
        self.stopStimulusBox.grid(row = 7, column = 1, sticky = 'w')

        # Forced decisions checkBox
        self.forcedDecisionRNG = np.random.default_rng(seed = None)
        self.forcedDecisions = 0   # probability; float between 0 and 1
        self.forcedDecisionEntry = tk.Entry(frame22, font = 8, width = 14)
        self.forcedDecisionEntry.insert(0, self.forcedDecisions)
        self.forcedDecisionEntry.grid(row = 8, column = 1, sticky = 'w')
        
        
        """
        Experiment Data
        
        """
        
        # Rig ID entry
        self.rigID = "mazeRig"
        self.rigEntry = tk.Entry(frame22, font = 8, width = 14)
        self.rigEntry.insert(0, self.rigID)
        self.rigEntry.grid(row = 1, column = 3, sticky ='w')
        
        # Animal ID entry
        self.animalID = "J000NC"
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
        tk.Label(frame13, font = buttonFont, text = "Behavior", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'we')
        labelList = ["performance", "bias index", "alternation index", "trials", "correct", "incorrect", "left decisions", "right decisions", "reward (μL)"]
        nrow = 1
        for i in range(len(labelList)):
            tk.Label(frame13, font = buttonFont, text = labelList[i], width = 14, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
            
        # Behavior parameters
        self.performance = 0
        self.biasIndex = 0
        self.alternationIndex = 0
        self.trialID = 0
        self.correct = 0
        self.incorrect = 0
        self.left = 0
        self.right = 0
        
        # RNG for randomizing trials
        self.mazeRNG = np.random.default_rng(seed = None)
        
        # Reward
        self.estimatedReward = 0
        self.leftRewardStreak = [32, 36, 41, 45, 49, 54] # in ms
        self.rightRewardStreak = [32, 37, 41, 46, 50, 55] # in ms
        self.rewardAmounts = [ 5,  6,  7,  8,  9, 10] # in μL
        
        # Behavior values in GUI
        self.performanceValue = tk.Label(frame13, font = buttonFont, text = self.performance)
        self.performanceValue.grid(row = 1, column = 1)
        self.biasIndexValue = tk.Label(frame13, font = buttonFont, text = self.biasIndex)
        self.biasIndexValue.grid(row = 2, column = 1)
        self.alternationIndexValue = tk.Label(frame13, font = buttonFont, text = self.alternationIndex)
        self.alternationIndexValue.grid(row = 3, column = 1)
        self.trialValue = tk.Label(frame13, font = buttonFont, text = self.trialID)
        self.trialValue.grid(row = 4, column = 1)
        self.correctValue = tk.Label(frame13, font = buttonFont, text = self.correct)
        self.correctValue.grid(row = 5, column = 1)
        self.incorrectValue = tk.Label(frame13, font = buttonFont, text = self.incorrect)
        self.incorrectValue.grid(row = 6, column = 1)
        self.leftValue = tk.Label(frame13, font = buttonFont, text = self.left)
        self.leftValue.grid(row = 7, column = 1)
        self.rightValue = tk.Label(frame13, font = buttonFont, text = self.right)
        self.rightValue.grid(row = 8, column = 1)
        self.rewardValue = tk.Label(frame13, font = buttonFont, text = self.estimatedReward)
        self.rewardValue.grid(row = 9, column = 1)
        self.behaviorStats = [self.performance, self.biasIndex, self.alternationIndex, self.trialID, self.correct, self.incorrect, self.left,self.right, self.estimatedReward]
        self.behaviorValues = [self.performanceValue, self.biasIndexValue, self.alternationIndexValue, self.trialValue, self.correctValue, self.incorrectValue, self.leftValue, self.rightValue, self.rewardValue]
        
        
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
        Connection with Acquisition Panel
        
        """
        
        # Acquisition panel controls
        self.controlPanelAddress = configurationData["acquisitionControlPanel"]["controlPanelAddress"]
        self.acquisitionPanelConnection = False
        self.command = None
        
        # Connect to acquisition panel
        self.connectToPanelButton = tk.Button(frame22, text = 'Connect', font = buttonFont, width = 17, command = self.startConnection)
        self.connectToPanelButton.grid(row = 7, column = 2, columnspan = 2, padx = 10, pady = 10)
        self.connectToPanelButton.bind('<Enter>', lambda e: self.connectToPanelButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.connectToPanelButton.bind('<Leave>', lambda e: self.connectToPanelButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Close connection with acquisition panel
        self.disconnectFromPanelButton = tk.Button(frame22, text = 'Disconnect', font = buttonFont, width = 17, command = self.closeConnection)
        self.disconnectFromPanelButton.grid(row = 8, column = 2, columnspan = 2, padx = 10, pady = 10)
        self.disconnectFromPanelButton.bind('<Enter>', lambda e: self.disconnectFromPanelButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.disconnectFromPanelButton.bind('<Leave>', lambda e: self.disconnectFromPanelButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        
        """
        Camera Controls
        
        """
        
        # Cameras
        eyeCameraID = int(configurationData["crownCameras"]["eyeCamera"])
        worldCameraID = int(configurationData["crownCameras"]["worldCamera"])
        self.cameraIDs = [eyeCameraID, worldCameraID]
        
        # Camera labels
        tk.Label(frame41, font = buttonFont, text = "Camera Controls", width = 12, anchor  = 'c').grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'we')
        
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
        Open Ephys Controls
        
        """
        
        # Path for Open Ephys exe
        self.OpenEphysPath = configurationData["openEphys"]["openEphysPath"]
        
        # Open Ephys labels
        tk.Label(frame42, font = buttonFont, text = "Ephys and IMU Controls", width = 25, anchor  = 'c').grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'we')
        
        # Initialize Open Ephys GUI
        self.launchOpenEphysButton = tk.Button(frame42, text = 'Launch Open Ephys', font = buttonFont, width = 17, command = self.launchOpenEphysGUI)
        self.launchOpenEphysButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.launchOpenEphysButton.bind('<Enter>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.launchOpenEphysButton.bind('<Leave>', lambda e: self.launchOpenEphysButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Preview
        self.previewOpenEphysButton = tk.Button(frame42, text = 'Preview Off', font = buttonFont, width = 17, command = self.previewOpenEphysChannels)
        self.previewOpenEphysButton.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='#99D492'))
        self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Start recording
        self.startEphysRecordingButton = tk.Button(frame42, text = 'Start Recording', font = buttonFont, width = 17, command = self.startEphysRecording)
        self.startEphysRecordingButton.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.startEphysRecordingButton.bind('<Enter>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='#DC5B5B'))
        self.startEphysRecordingButton.bind('<Leave>', lambda e: self.startEphysRecordingButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Stop recording
        self.stopEphysRecordingButton = tk.Button(frame42, text = 'Stop Recording', font = buttonFont, width = 17, command = self.stopEphysRecording)
        self.stopEphysRecordingButton.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.stopEphysRecordingButton.bind('<Enter>', lambda e: self.stopEphysRecordingButton.config(fg = 'Black', bg ='#FFB844'))
        self.stopEphysRecordingButton.bind('<Leave>', lambda e: self.stopEphysRecordingButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Close Open Ephys GUI
        self.closeOpenEphysGUIButton = tk.Button(frame42, text = 'Close Open Ephys', font = buttonFont, width = 17, command = self.closeOpenEphysGUI)
        self.closeOpenEphysGUIButton.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.closeOpenEphysGUIButton.bind('<Enter>', lambda e: self.closeOpenEphysGUIButton.config(fg = 'Black', bg ='#AFAFAA'))
        self.closeOpenEphysGUIButton.bind('<Leave>', lambda e: self.closeOpenEphysGUIButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        
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
        
        # Stimulus trigger sensors
        self.startStimulusIRsensor = int(configurationData["teensyConfiguration"]["startStimulusIRsensor"])
        self.stopStimulusIRsensor = int(configurationData["teensyConfiguration"]["stopStimulusIRsensor"])
        
        # Water ports and LEDs
        self.leftWaterPort = int(configurationData["teensyConfiguration"]["leftWaterPort"])
        self.rightWaterPort = int(configurationData["teensyConfiguration"]["rightWaterPort"])
        self.leftLED = int(configurationData["teensyConfiguration"]["leftLED"])
        self.rightLED = int(configurationData["teensyConfiguration"]["rightLED"])
        
        # Labels and pin states in GUI
        self.sensorLabelValues = [self.leftStartValue, self.rightStartValue, self.leftDecisionValue, self.rightDecisionValue, self.startStimulusValue, self.stopStimulusValue]
        self.pinStates = [self.LS,self.RS,self.LD,self.RD, self.stimulusOn, self.stimulusOff]
        
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
            self.board.get_pin('d:'+str(self.startStimulusIRsensor)+':i')
            self.board.get_pin('d:'+str(self.stopStimulusIRsensor)+':i')
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
                self.mazeStateLabel.config(bg = self.backGroundColor, text = "idle")
                self.mazeStateValue.config(text = 0)
                self.leftStartLabel.config(bg = '#99D492', text = "open")
                self.rightStartLabel.config(bg = '#99D492', text = "open")
                self.leftDecisionLabel.config(bg = '#99D492', text = "open")
                self.rightDecisionLabel.config(bg = '#99D492', text = "open")
                self.leftDecisionValue.config(text = 0)
                self.rightDecisionValue.config(text = 0)
                self.leftStartValue.config(text = 0)
                self.rightStartValue.config(text = 0)
                self.stimulusStateLabel.config(bg = self.backGroundColor, text = "idle")
                self.stimulusStateValue.config(text = 0)
                self.startStimulusLabel.config(bg = self.backGroundColor, text = "idle")
                self.stopStimulusLabel.config(bg = self.backGroundColor, text = "idle")
                self.startStimulusValue.config(text = 0)
                self.stopStimulusValue.config(text = 0)
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
            self.leftStartLabel.config(bg = 'pink', text = "closed")
            self.rightStartLabel.config(bg = 'pink', text = "closed")
            if (self.blockIncorrectDoor == 1 and self.targetLocation == 0) or self.blockIncorrectDoor == 0:
                self.board.digital[self.leftDecisionDoor].write(0)
                self.leftDecisionLabel.config(bg = '#99D492', text = "open")
            if (self.blockIncorrectDoor == 1 and self.targetLocation == 1) or self.blockIncorrectDoor == 0:
                self.board.digital[self.rightDecisionDoor].write(0)
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
    
    def updateStimulusDisplay(self):
        
        # Before trial start
        if self.stimulusState == 0:
            self.stimulusStateLabel.config(bg = '#A9C6E3', text = "ready")
            self.stimulusStateValue.config(text = 0)
            if self.stimulusOnSwitch == True:
                self.startStimulusLabel.config(bg = '#A9C6E3', text = "ready")
            if self.stimulusOffSwitch == True:
                self.stopStimulusLabel.config(bg = '#A9C6E3', text = "ready")
            
        # After trial start, waiting to trigger stimulus
        elif self.stimulusState == 1:
            self.stimulusStateValue.config(text = 1)
            if self.stimulusOnSwitch == True:
                self.stimulusStateLabel.config(bg = 'pink', text = "off")
                self.startStimulusLabel.config(bg = 'pink', text = "off")
            elif self.stimulusOnSwitch == False:
                self.stimulusStateLabel.config(bg = '#99D492', text = "on")
            if self.stimulusOffSwitch == True:
                self.stopStimulusLabel.config(bg = 'pink', text = "off")
            
        # Stimulus is on
        elif self.stimulusState == 2:
            self.stimulusStateValue.config(text = 2)
            if self.stimulusOnSwitch == True:
                self.visualStimulus.startStimulus(display = True)
                self.dataFrameStimulusStartTime.append(time.time() - self.taskTimeStart)
                self.stimulusIsOn = True
                self.stimulusStateLabel.config(bg = '#99D492', text = "on")
                self.startStimulusLabel.config(bg = '#99D492', text = "on")
        
        # Stimulus is off
        elif self.stimulusState == 3:
            self.stimulusStateValue.config(text = 3)
            if self.stimulusOnSwitch == True and self.stimulusOffSwitch == True:
                self.startStimulusLabel.config(bg = 'pink', text = "off")
            if self.stimulusOffSwitch == True:
                self.visualStimulus.stopStimulus(display = False)
                self.dataFrameStimulusEndTime.append(time.time() - self.taskTimeStart)
                self.stimulusIsOn = False
                self.stimulusStateLabel.config(bg = 'pink', text = "off")
                self.stopStimulusLabel.config(bg = '#99D492', text = "on")
        
        # Waiting for decision after stimulus is off
        elif self.stimulusState == 4:
            self.stimulusStateValue.config(text = 4)
            if self.stimulusOffSwitch == True:
                self.stopStimulusLabel.config(bg = 'pink', text = "off")
                # Fail-safe: in case stimulus is not turned off
                if self.stimulusIsOn == True:
                    self.visualStimulus.stopStimulus(display = False)
                    self.dataFrameStimulusEndTime.append(None)
                    self.stimulusIsOn = False
            elif self.stimulusOffSwitch == False:
                self.stimulusStateLabel.config(bg = 'pink', text = "off")
                self.startStimulusLabel.config(bg = 'pink', text = "off")
            
        # Waiting for new trial to begin
        elif self.stimulusState == 5:
            self.stimulusStateLabel.config(bg = '#A9C6E3', text = "ready")
            self.stimulusStateValue.config(text = 5)
            if self.stimulusOnSwitch == True:
                self.startStimulusLabel.config(bg = '#A9C6E3', text = "ready")
            if self.stimulusOffSwitch == True:
                self.stopStimulusLabel.config(bg = '#A9C6E3', text = "ready")
                
    def readPinStates(self):
        
        # Read pins
        self.LD = self.board.digital[self.leftDecisionIRsensor].read()
        self.RD = self.board.digital[self.rightDecisionIRsensor].read()
        self.LS = self.board.digital[self.leftStartIRsensor].read()
        self.RS = self.board.digital[self.rightStartIRsensor].read()
        self.stimulusOn = self.board.digital[self.startStimulusIRsensor].read()
        self.stimulusOff = self.board.digital[self.stopStimulusIRsensor].read()

        # Update IR sensor values in GUI
        self.sensorLabelValues = [self.leftStartValue, self.rightStartValue, self.leftDecisionValue, self.rightDecisionValue, self.startStimulusValue, self.stopStimulusValue]
        self.pinStates = [self.LS,self.RS,self.LD,self.RD, self.stimulusOn, self.stimulusOff]
        for i in range(len(self.sensorLabelValues)):
            if self.pinStates[i] is False:
                self.sensorLabelValues[i].config(text = 0)
            elif self.LD is True or self.RD is True:
                self.sensorLabelValues[i].config(text = 1)
            self.sensorLabelValues[i].update_idletasks()
            
    def updateMazeState(self):
        
        # Maze state
        self.currentMazeState = self.mazeState
        
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
            if self.reward is False and self.initializeTrial is True:
                self.initializeUpcomingTrial()
                self.initializeTrial = False
            if time.time() > self.interTrialStart + self.interTrialTimeOut:
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
        if self.currentMazeState != self.mazeState:
            self.updateDoors()

    def updateStimulusState(self):
        
        # Stimulus state
        self.currentStimulusState = self.stimulusState
        
        # Update stimulus states
        if self.stimulusState == 1:
            if self.stimulusOn == False:
                self.stimulusState = 2
        elif self.stimulusState == 2:
            if self.stimulusOff == False:
                self.stimulusState = 3
            # Fail-safe: in case stimulus is not turned off
            elif self.mazeState == 2:
                self.stimulusState = 4
        elif self.stimulusState == 3:
            if self.mazeState == 2:
                self.stimulusState = 4
        elif self.stimulusState == 4:
            if self.mazeState == 3 or self.mazeState == 4:
                self.stimulusState = 5
        elif self.stimulusState == 5:
            if self.mazeState == 1:
                self.stimulusState = 1
        
        # Update stimulus
        if self.currentStimulusState != self.stimulusState:
            self.updateStimulusDisplay()

    def closeValve(self):
        
        # Close valve
        while self.reward is True:
            if time.time() > self.rewardStart + self.rewardTime:
                self.board.digital[self.waterPort].write(0)
                self.board.digital[self.LED].write(0)
                self.reward = False
            
    def giveReward(self):
        
        # Trigger reward
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
        
        # Check on valve
        self.rewardThread = Thread(target = self.closeValve())
        self.rewardThread.start()


    """ 
    Connection with Acquisition Panel
    
    """

    def startConnection(self):
        
        if self.acquisitionPanelConnection is False:
            
            # Initialize Maze GUI socket (client)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.client.connect(('127.0.0.1', 12345))
            self.client.connect((self.controlPanelAddress, 12345)) 
            self.acquisitionPanelConnection = True
            print("Connection with Acquisition Panel is ready.")
            
            # Thread to handle initialization of camera feed
            self.listenToServer = Thread(target = self.checkOnServer())
            self.listenToServer.start()
            
            # Update connectToPanelButton: connection has been established...
            self.connectToPanelButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Connected')
            self.connectToPanelButton.bind('<Enter>', lambda e: self.connectToPanelButton.config(fg = 'Blue', bg ='#A9C6E3'))
            self.connectToPanelButton.bind('<Leave>', lambda e: self.connectToPanelButton.config(fg = 'Blue', bg = '#A9C6E3'))
            self.connectToPanelButton.update_idletasks()
            
        elif self.acquisitionPanelConnection is True:
            
            print("Acquisition Panel is not available. It might be already connected.")

    def closeConnection(self):
        
        if self.acquisitionPanelConnection is True:
            
            # Close Maze GUI socket (client)
            self.command = ["closeConnection", False]
            self.command = pickle.dumps(self.command)
            self.client.send(self.command)
            self.client.close()
            self.acquisitionPanelConnection = False
            print("Connection with Acquisition Panel has now been been closed.")
            
            # Reset connectToPanelButton
            self.connectToPanelButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Connect')
            self.connectToPanelButton.bind('<Enter>', lambda e: self.connectToPanelButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.connectToPanelButton.bind('<Leave>', lambda e: self.connectToPanelButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.connectToPanelButton.update_idletasks()
            
            # Final checks
            try:
                self.crownCameras
            except:
                ... # Crown cameras have been properly closed
            else:
                self.closeCameras()
            try:
                self.openEphys
            except:
                ... # Open Ephys has been properly closed
            else:
                self.closeOpenEphysGUI()
            
        elif self.acquisitionPanelConnection is False:
            
            print("Connection with Acquisition Panel has not been established yet.")
        
    def checkOnServer(self):
        
        if self.acquisitionPanelConnection is True:
            
            # Read data from Acquisition Panel (server)
            listenToServer, _, _ = select.select([self.client], [], [], 0.05)
            for s in listenToServer:
                if s == self.client:
                    data = s.recv(1024)
                    if data:
                        try:
                            serverData = pickle.loads(data)
                            if serverData[0] == "closeConnection":
                                self.closeConnection()
                        except pickle.UnpicklingError:
                            print("Error processing client data.")
            
            # Loop
            self.mainWindow.after(1000, self.checkOnServer)
        

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
            self.updateTrialSettings()
            sessionInfo = [self.animalID, self.currentDate, self.blockID]
            
            # Initialize crown cameras locally
            if self.acquisitionPanelConnection is False:
                
                self.crownCameras = crownCameras.crownCameras(self.cameraIDs, self.pathForSavingData , sessionInfo)
                
            # Initialize crown cameras in Acquisition Panel (server)
            elif self.acquisitionPanelConnection is True:
                
                # Prepare local camera object
                class shamCameraObject:
                    pass
                self.crownCameras = shamCameraObject()
                
                # Input for camera object
                dataForServer = ["cameraInput", self.cameraIDs, sessionInfo]
                dataForServer = pickle.dumps(dataForServer)
                self.client.send(dataForServer)
                time.sleep(1)
                
                # Initialize camera object in Acquisition Panel (server)
                self.command = ["initializeCameras"]
                self.command = pickle.dumps(self.command)
                self.client.send(self.command)
                time.sleep(1)
                
                # Retrieve data from Acquisition Panel (server)
                data = self.client.recv(1024)
                serverData = pickle.loads(data)
                self.crownCameras.camerasAreOn = serverData[0]
                self.crownCameras.eyeCameraAvailable = serverData[1]
                self.crownCameras.worldCameraAvailable = serverData[2]
                
            if self.crownCameras.eyeCameraAvailable is True and self.crownCameras.worldCameraAvailable is True:
                
                if self.crownCameras.camerasAreOn is True:
                    
                    # Update startCameraButton: cameras are open (preview mode)...
                    self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Preview')
                    self.startCameraButton.bind('<Enter>', lambda e: self.startCameraButton.config(fg = 'Blue', bg ='#A9C6E3'))
                    self.startCameraButton.bind('<Leave>', lambda e: self.startCameraButton.config(fg = 'Blue', bg = '#A9C6E3'))
                    self.startCameraButton.update_idletasks()
                    
                    if self.acquisitionPanelConnection is False:
                        
                        # Start camera feed (preview)
                        self.crownCameras.startCameras()
                    
                    elif self.acquisitionPanelConnection is True:

                        # Start camera feed (preview) in Acquisition Panel (server)
                        self.command = ["startCameras"]
                        self.command = pickle.dumps(self.command)
                        self.client.send(self.command)
                        
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
                
                if self.acquisitionPanelConnection is True:
                    
                    # Delete camera object in Acquisition Panel (server)
                    self.command = ["deleteCameras"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                
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
                
            if self.acquisitionPanelConnection is False:
    
                # Start video recording
                try:
                    self.crownCameras.recordVideo()
                except:
                    print("Connection stopped unexpectedly. You can control cameras from the Acquisition Control Panel.")
    
            elif self.acquisitionPanelConnection is True:
    
                # Start video recording in Acquisition Panel (server)
                self.command = ["recordVideo"]
                self.command = pickle.dumps(self.command)
                self.client.send(self.command)
                time.sleep(1)
                
                # Retrieve data from Acquisition Panel (server)
                data = self.client.recv(1024)
                serverData = pickle.loads(data)
                self.crownCameras.saveVideo = serverData[0]
        
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
                
            if self.acquisitionPanelConnection is False:
    
                # Stop video recording
                try:
                    self.crownCameras.stopVideo()
                except:
                    print("Connection stopped unexpectedly. You can control cameras from the Acquisition Control Panel.")
    
            elif self.acquisitionPanelConnection is True:
    
                # Stop video recording in Acquisition Panel (server)
                self.command = ["stopVideo"]
                self.command = pickle.dumps(self.command)
                self.client.send(self.command)
                time.sleep(1)
                
                # Retrieve data from Acquisition Panel (server)
                data = self.client.recv(1024)
                serverData = pickle.loads(data)
                self.crownCameras.saveVideo = serverData[0]
        
        
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
    
            if self.acquisitionPanelConnection is False:
    
                # Close crown cameras
                try:
                    self.crownCameras.closeCameras()
                except:
                    print("Connection stopped unexpectedly. You can control cameras from the Acquisition Control Panel.")
    
            elif self.acquisitionPanelConnection is True:
    
                # Close crown cameras in Acquisition Panel (server)
                self.command = ["closeCameras"]
                self.command = pickle.dumps(self.command)
                self.client.send(self.command)
                time.sleep(1)
                
                # Retrieve data from Acquisition Panel (server)
                data = self.client.recv(1024)
                serverData = pickle.loads(data)
                self.crownCameras.camerasAreOn = serverData[0]
                self.crownCameras.saveVideo = serverData[1]
                
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
            self.updateTrialSettings()
            sessionInfo = [self.animalID, self.currentDate, self.blockID]    
        
            # Launch Open Ephys GUI locally
            if self.acquisitionPanelConnection is False:
                
                self.openEphys = openEphys.openEphys(self.OpenEphysPath, self.pathForSavingData , sessionInfo)
                
            # Launch Open Ephys from Acquisition Panel (server)
            elif self.acquisitionPanelConnection is True:
                
                # Prepare local Open Ephys object
                class shamOpenEphysObject:
                    pass
                self.openEphys = shamOpenEphysObject()
        
                # Input for Open Ephys object
                dataForServer = ["launchOpenEphys", sessionInfo]
                dataForServer = pickle.dumps(dataForServer)
                self.client.send(dataForServer)
                time.sleep(1)
                
                # Retrieve data from Acquisition Panel (server)
                data = self.client.recv(1024)
                serverData = pickle.loads(data)
                self.openEphys.OpenEphysGUIHasBeenLaunched = serverData[0]
                self.openEphys.ephysPreviewIsOn = serverData[1]
                self.openEphys.ephysRecordingInProgress = serverData[2]
                
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
                
                if self.acquisitionPanelConnection is False:
                
                    # Start preview mode
                    self.openEphys.previewOpenEphysChannels()
                    
                elif self.acquisitionPanelConnection is True:
                    
                    # Start preview mode in Acquisition Panel (server)
                    self.command = ["previewOpenEphysChannels"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                    
                    # Retrieve data from Acquisition Panel (server)
                    data = self.client.recv(1024)
                    serverData = pickle.loads(data)
                    self.openEphys.ephysPreviewIsOn = serverData[0]
            
            elif self.openEphys.OpenEphysGUIHasBeenLaunched is True and self.openEphys.ephysPreviewIsOn is True and self.openEphys.ephysRecordingInProgress is False:
                
                # Update previewOpenEphysButton: preview mode...
                self.previewOpenEphysButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Preview Off')
                self.previewOpenEphysButton.bind('<Enter>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg ='#99D492'))
                self.previewOpenEphysButton.bind('<Leave>', lambda e: self.previewOpenEphysButton.config(fg = 'Black', bg = 'SystemButtonFace'))
                self.previewOpenEphysButton.update_idletasks()
                
                if self.acquisitionPanelConnection is False:
                
                    # Stop preview mode
                    self.openEphys.previewOpenEphysChannels()
                    
                elif self.acquisitionPanelConnection is True:
                    
                    # Stop preview mode in Acquisition Panel (server)
                    self.command = ["previewOpenEphysChannels"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                    
                    # Retrieve data from Acquisition Panel (server)
                    data = self.client.recv(1024)
                    serverData = pickle.loads(data)
                    self.openEphys.ephysPreviewIsOn = serverData[0] 
            
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
                
                if self.acquisitionPanelConnection is False:
                
                    # Start ephys recording
                    try:
                        self.openEphys.startEphysRecording()
                    except:
                        print("Connection stopped unexpectedly. You can control Open Ephys from the Acquisition Control Panel.")
                    
                elif self.acquisitionPanelConnection is True:
                    
                    # Start ephys recording in Acquisition Panel (server)
                    self.command = ["startEphysRecording"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                    
                    # Retrieve data from Acquisition Panel (server)
                    data = self.client.recv(1024)
                    serverData = pickle.loads(data)
                    self.openEphys.ephysRecordingInProgress = serverData[0]
        
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
                
                if self.acquisitionPanelConnection is False:
                    
                    # Stop ephys recording
                    try:
                        self.openEphys.stopEphysRecording()
                    except:
                        print("Connection stopped unexpectedly. You can control Open Ephys from the Acquisition Control Panel.")
                    
                    
                elif self.acquisitionPanelConnection is True:
                    
                    # Stop ephys recording in Acquisition Panel (server)
                    self.command = ["stopEphysRecording"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                    
                    # Retrieve data from Acquisition Panel (server)
                    data = self.client.recv(1024)
                    serverData = pickle.loads(data)
                    self.openEphys.ephysRecordingInProgress = serverData[0]
        
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
                
                if self.acquisitionPanelConnection is False:
                
                    # Close Open Ephys GUI
                    try:
                        self.openEphys.closeOpenEphysGUI()
                    except:
                        print("Connection stopped unexpectedly. You can control Open Ephys from the Acquisition Control Panel.")
                
                elif self.acquisitionPanelConnection is True:
                
                    # Close Open Ephys GUI in Acquisition Panel (server)
                    self.command = ["closeOpenEphys"]
                    self.command = pickle.dumps(self.command)
                    self.client.send(self.command)
                    time.sleep(1)
                    
                    # Retrieve data from Acquisition Panel (server)
                    data = self.client.recv(1024)
                    serverData = pickle.loads(data)
                    self.openEphys.OpenEphysGUIHasBeenLaunched = serverData[0]
                
                # Delete camera object
                del self.openEphys

    
    """ 
    Task Functions
    
    """    
    
    def initializeTaskParameters(self):
        
        # Task
        self.runningTask = False
        self.initializeTrial = True
        self.stimulusIsOn = False
        self.interTrialStart = 0
        self.interTrialTimeOut = 0
        self.correctInterTrialTimeOut = 3
        self.incorrectInterTrialTimeOut = 15
        self.probabilityTargetLeft = 0.5
        self.targetLocation = None
        
        # Behavior stats
        self.performance = 0
        self.biasIndex = 0
        self.alternationIndex = 0
        self.trialID = 0
        self.correct = 0
        self.incorrect = 0
        self.left = 0
        self.right = 0
        self.trialType = 0
        self.lastDecision = None
        self.decisionAlternations = 0
        
        # Recent behavior
        self.recentPerformance = 0
        self.recentBiasIndex = 0
        self.recentBiasDecisions = []
        self.recentAlternationIndex = 0
        self.recentSwitchDecisions = []
        
        # Reward
        self.reward = False
        self.rewardSize = 0
        self.rewardStart = 0
        self.rewardTime = 0
        self.estimatedReward = 0
        self.correctStreak = 0
        self.waterPort = None
        self.LED = None
        
        # Experiment data
        self.dataFrameTrial = []
        self.dataFrameTarget = []
        self.dataFrameDecision = []
        self.datFrameForcedDecision = []
        self.dataFrameCorrect = []
        self.dataFrameTrialType = []
        self.dataFrameStartDoor = []
        self.dataFrameLeftProbability = []
        self.dataFrameTimeStampOffest = []
        self.dataFrameStartTime = []
        self.dataFrameEndTime = []
        self.dataFrameStimulusStartTime = []
        self.dataFrameStimulusEndTime = []
        self.dataFrameRawTaskStartTime = []
    
        # Update behavior stats in GUI
        self.updateBehaviorStats()
    
    def updateTrialSettings(self):
        
        # Input task settings
        self.maximumTrialNumber = int(self.trialsEntry.get())
        self.timeout = int(self.timeEntry.get())
        self.taskName = str(self.taskBox.get())
        self.startDoor = str(self.startBox.get())
        self.trialCues = bool(self.useTrialCues.get())
        self.stimulusOnSwitch = bool(self.startStimulusTrigger.get())
        self.stimulusOffSwitch = bool(self.stopStimulusTrigger.get())
        self.forcedDecisions = float(self.forcedDecisionEntry.get())
        self.animalID = str(self.animalEntry.get())
        self.rigID = str(self.rigEntry.get())
        self.blockID = str(self.blockEntry.get())
        self.autoSave = bool(self.autoSaveData.get())
    
    def retrieveTaskParameters(self):
        
        # Table for task settings
        taskSettings = {
                          "rigID": self.rigID,              
                          "animalID": self.animalID,
                          "blockID": str(self.blockID),
                          "taskName": self.taskName,
                          "maximumNumberOfTrials": str(self.maximumTrialNumber),
                          "maximumSessionTime": str(self.timeout),
                          "initialStartDoor": self.startDoor,
                          "useSoundCues": str(self.trialCues),
                          "startStimulusTrigger": str(self.stimulusOnSwitch),
                          "stopStimulusTrigger": str(self.stimulusOffSwitch),
                          "forcedDecisionProbability": str(self.forcedDecisions),
                          "initialLeftTargetProbability": str(self.probabilityTargetLeft),
                          "correctInterTrialTimeOut": str(self.correctInterTrialTimeOut),
                          "incorrectInterTrialTimeOut": str(self.incorrectInterTrialTimeOut),
                          "rewardAmounts": str(self.rewardAmounts),
                          "leftRewardStreak": str(self.leftRewardStreak),
                          "rightRewardStreak": str(self.rightRewardStreak),
                                                                               }
        taskSettings = pd.DataFrame.from_dict(taskSettings, orient = 'index')

        # Table for stimulus settings
        stimulusParameters = self.visualStimulus.retrieveStimulusParameters()
    
        # Concatenate both tables
        taskParameters = [taskSettings, stimulusParameters]
        taskParameters = pd.concat(taskParameters)
        taskParameters = taskParameters.transpose()
        self.taskParameters = taskParameters
    
    def readyTask(self):
        
        # Check if Teensy 4.0 is available before attempting to initialize a task
        boardAvailable = self.checkIfPortAvailable()
        
        if boardAvailable is True:
        
            # Update task settings
            self.updateTrialSettings()
            
            # Flush all data from previous task
            self.initializeTaskParameters()
            
            # Display task settings when initializing task
            print(" ")
            if not self.taskName == "valveCalibration":
                # Display on terminal
                print("     Task Settings:")
                print("          Rig ID:", self.rigID)
                print("          Animal ID:", self.animalID)
                print("          Block ID:", self.blockID)
                print("          Task name:", self.taskName)
                print("          Maximum number of trials:", self.maximumTrialNumber)
                print("          Maximum session time (s):", self.timeout)
                print("          Start door:", self.startDoor)
                print("          Use sound cues:", str(self.trialCues).lower())
                print("          Start stimulus trigger:", str(self.stimulusOnSwitch).lower())
                print("          Stop stimulus trigger:", str(self.stimulusOffSwitch).lower())
                print("          Forced decision probability = ", str(self.forcedDecisions))
                print("          AutoSave:", self.autoSave)
            else:
                # Display calibration curve example on terminal
                print(" ")
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
                    self.mazeState = 0
                    self.updateDoors()
                    if self.stimulusOnSwitch == True or self.stimulusOffSwitch == True:
                        self.stimulusState = 0
                        self.updateStimulusDisplay()
                
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
                entryBoxes = [self.taskSettingsLabel, self.trialsEntry, self.timeEntry, self.taskBox, self.startBox, self.cuesBox, self.startStimulusBox, self.stopStimulusBox, self.forcedDecisionEntry,
                              self.experimentDataLabel, self.animalEntry, self.rigEntry, self.blockEntry, self.pathEntry, self.autoSaveBox]
                for i in range(len(entryBoxes)):
                    entryBoxes[i].config(state = 'disabled')
                    entryBoxes[i].update_idletasks()
                # Retrieve task and stimulus settings (for now, it will only work for driftingGratings)
                if self.taskName == "driftingGratings":
                    self.retrieveTaskParameters()
                # Prepare first trial
                self.initializeUpcomingTrial()
                
        else:
            
            # Handle cases when Teensy 4.0 is not available
            if self.runningTask is True:
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
        entryBoxes = [self.taskSettingsLabel, self.trialsEntry, self.timeEntry, self.taskBox, self.startBox, self.cuesBox, self.startStimulusBox, self.stopStimulusBox, self.forcedDecisionEntry,
                      self.experimentDataLabel, self.animalEntry, self.rigEntry, self.blockEntry, self.pathEntry, self.autoSaveBox]
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
        
        # Forced decision for upcoming trial
        if self.forcedDecisions > 0 and self.forcedDecisions <= 1:
            self.blockIncorrectDoor = self.forcedDecisionRNG.choice([0,1], p = [1-self.forcedDecisions, self.forcedDecisions])
            if self.blockIncorrectDoor == 1:
                self.forcedDecisionLabel = "[forced decision]"
            else:
                self.forcedDecisionLabel = " "
        else:
            self.blockIncorrectDoor = 0
            self.forcedDecisionLabel = " "
        
        # Upcoming viual stimulus
        self.visualStimulus.initializeStimulus(target = self.targetLocation)
        
        # Reward for upcoming trial
        if self.correctStreak < len(self.rewardAmounts):
            if self.targetLocation == 0:
                self.rewardTime = self.leftRewardStreak[self.correctStreak] / 1000 # in s
            elif self.targetLocation  == 1:
                self.rewardTime = self.rightRewardStreak[self.correctStreak] / 1000 # in s
            self.rewardSize = self.rewardAmounts[self.correctStreak] # in μL
        else:
            if self.targetLocation == 0:
                self.rewardTime = self.leftRewardStreak[-1] / 1000 # in s
            elif self.targetLocation == 1:
                self.rewardTime = self.rightRewardStreak[-1] / 1000 # in s
            self.rewardSize = self.rewardAmounts[-1] # in μL
            
    def startTrial(self):
        
        # Display trial info in terminal
        if self.targetLocation == 0:
            targetLabel = "Left"
        elif self.targetLocation == 1:
            targetLabel = "Right"
        self.trialID += 1
        print("     Trial", self.trialID, "started...", " Target ->", targetLabel, "@ p =", self.probabilityTargetLeft, "(Left)")
        
        # Display visual stimulus
        if self.stimulusOnSwitch == False:
            self.visualStimulus.startStimulus(display = True)
            self.dataFrameStimulusStartTime.append(None)
        
        # Append experiment data to data frame
        self.dataFrameStartTime.append(time.time() - self.taskTimeStart)
        self.dataFrameTrial.append(self.trialID)
        self.dataFrameTarget.append(self.targetLocation)
        if self.startDoor == "left":
            self.dataFrameStartDoor.append(0)
        elif self.startDoor == "right":
            self.dataFrameStartDoor.append(1)
            
    def endTrial(self):
        
        # Trial outcome
        self.triggerTrialOutcome()
        
        # End visual stimulus
        if self.stimulusOffSwitch is False:
            self.visualStimulus.stopStimulus(display = False)
            self.dataFrameStimulusEndTime.append(None)
            
        # Grab time stamp offset
        self.timeStampOffest = ntplib.NTPClient().request('pool.ntp.org').offset
        self.dataFrameTimeStampOffest.append(self.timeStampOffest)
        if self.acquisitionPanelConnection is True:
            self.command = ["grabTimeOffset", False]
            self.command = pickle.dumps(self.command)
            self.client.send(self.command)
        
        # Append experiment data to data frame
        self.dataFrameDecision.append(self.lastDecision)
        self.datFrameForcedDecision.append(self.blockIncorrectDoor)
        self.dataFrameTrialType.append(self.trialType)
        self.dataFrameEndTime.append(time.time() - self.taskTimeStart)
        if self.trialType == 1 or self.trialType == 4:
            self.dataFrameCorrect.append(1)
        elif self.trialType == 2 or self.trialType == 3:
            self.dataFrameCorrect.append(0)
        self.dataFrameLeftProbability.append(self.probabilityTargetLeft)
        
        # Recent quick stats
        if self.trialID >= 10:
            recentCorrect = self.dataFrameCorrect[-10:]
            self.recentPerformance = round(recentCorrect.count(1) / len(recentCorrect), 2)
            
        # Bias correction
        if self.trialID >= 10:
            self.recentBiasDecisions = self.dataFrameDecision[-10:]
            self.recentBiasIndex = round((self.recentBiasDecisions.count(0) - self.recentBiasDecisions.count(1)) / len(self.recentBiasDecisions), 2)
           
        # Alternation correction
        if self.trialID >= 11:
            self.recentSwitchDecisions = self.dataFrameDecision[-11:]
            self.recentAlternationIndex = round(sum(abs(np.diff(self.recentSwitchDecisions))) / len(self.recentSwitchDecisions), 2)
        
        # Updated target probability
        if (abs(self.recentBiasIndex) >= (self.recentAlternationIndex - 0.5) ) and self.trialID >= 10:
            self.probabilityTargetLeft = 0.5 - (self.recentBiasIndex/2)
        elif ( (self.recentAlternationIndex - 0.5) > abs(self.recentBiasIndex)) and self.trialID >= 11:
            if self.lastDecision == 0:
                self.probabilityTargetLeft = 0.5 + (self.recentAlternationIndex - 0.5)
            elif self.lastDecision == 1:
                self.probabilityTargetLeft = 0.5 - (self.recentAlternationIndex - 0.5)
        self.probabilityTargetLeft = round(self.probabilityTargetLeft, 2)
        
        # Display stats on terminal
        if self.trialType == 1:
            print("          >>> Correct Left <<<   ", self.forcedDecisionLabel)
        elif self.trialType == 2:
            print("          --- Incorrect Left ---   ", self.forcedDecisionLabel)
        elif self.trialType == 3:
            print("          --- Incorrect Right ---   ", self.forcedDecisionLabel)
        elif self.trialType == 4:
            print("          >>> Correct Right <<<   ", self.forcedDecisionLabel)
        if self.trialID <= 10:
            print("              Performance = ", self.performance)
            print("              Bias index = ", self.biasIndex)
            if self.trialID > 1:
                print("              Alternation index = ", self.alternationIndex)
        else:
            print("              Performance (overall) = ", self.performance, "           Performance (recent)", self.recentPerformance)
            print("              Bias index (overall) = ", self.biasIndex,"           Bias index (recent) = ", self.recentBiasIndex)
            print("              Alternation index (overall) = ", self.alternationIndex,"     Alternation index (recent) = ", self.recentAlternationIndex)
        
        # Update behavior stats in GUI
        self.updateBehaviorStats()
        
        # End task after last trial
        if self.trialID == self.maximumTrialNumber:
            self.runningTask = False
            print(" ")
            print("The task has reached the maximum number of trials!")
        
    def updateBehaviorStats(self):
        
        # Update behavior stats in GUI
        self.behaviorStats = [self.performance, self.biasIndex, self.alternationIndex, self.trialID, self.correct, self.incorrect, self.left,self.right, self.estimatedReward]
        self.behaviorValues = [self.performanceValue, self.biasIndexValue, self.alternationIndexValue, self.trialValue, self.correctValue, self.incorrectValue, self.leftValue, self.rightValue, self.rewardValue]
        for i in range(len(self.behaviorValues)):
            self.behaviorValues[i].config(text = self.behaviorStats[i])
            self.behaviorValues[i].update_idletasks()
        
        
    def triggerTrialOutcome(self):
        
        # Trial type and outcome
        if self.LD is False:
            self.left += 1
            if self.trialID > 1:
                if self.lastDecision == 0:
                    ...
                elif self.lastDecision == 1:
                    self.decisionAlternations += 1
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
            if self.trialID > 1:
                if self.lastDecision == 0:
                    self.decisionAlternations += 1
                elif self.lastDecision == 1:
                    ...
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
        self.performance = round(self.correct / (self.correct + self.incorrect), 2)
        self.biasIndex = round((self.left-self.right) / (self.left+self.right), 2)
        if self.trialID > 1:
            self.alternationIndex = round(self.decisionAlternations / (self.trialID-1), 2)
        
    def runTask(self):
        
        if self.runningTask is False:
        
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
            if self.stimulusOnSwitch is True or self.stimulusOffSwitch is True:
                self.stimulusState = 5
                self.updateStimulusDisplay()
            self.runningTask = True
            self.timeStampOffest = None
            self.taskTimeStart = time.time()
            self.dataFrameRawTaskStartTime.append(self.taskTimeStart)
            print(" ")
            
            # Start task
            self.currentRunningTask = Thread(target = self.checkTask())
            self.currentRunningTask.start()
            
        else:
            
            print("There is an ongoing task currently running...")
    
    def checkTask(self):
        
        # Check IR sensors and update task states
        while self.runningTask is True:
            
            self.mainWindow.update()
            self.readPinStates()
            self.updateMazeState()
            if self.stimulusOnSwitch is True or self.stimulusOffSwitch is True:
                self.updateStimulusState()
            self.visualStimulus.updateStimulus()
            if time.time() > self.taskTimeStart + self.timeout:
                self.runningTask = False
                print(" ")
                print("The task has reached its time limit!")
            if self.runningTask is False:
                break
            
        # Reset task once it is finished
        if self.runningTask is False:
            self.resetTask()
            
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
        behaviorData = {
                "trial": self.dataFrameTrial,
                "startDoor": self.dataFrameStartDoor,
                "leftTargetProbability": self.dataFrameLeftProbability,
                "target": self.dataFrameTarget,
                "decision": self.dataFrameDecision,
                "forcedChoice": self.datFrameForcedDecision,
                "correct": self.dataFrameCorrect,
                "trialType": self.dataFrameTrialType,
                "timeOffset": self.dataFrameTimeStampOffest,
                "startTime": self.dataFrameStartTime,
                "endTime": self.dataFrameEndTime,
                "stimulusStartTime": self.dataFrameStimulusStartTime,
                "stimulusEndTime": self.dataFrameStimulusEndTime,
                "taskRawStartTime": self.dataFrameRawTaskStartTime,
                                                                   }
        behaviorData = pd.DataFrame.from_dict(behaviorData, orient = 'index')
        behaviorData = behaviorData.transpose()
        
        # Concatenate behavior data and task parameters (for now, it will only work for driftingGratings)
        if self.taskName == "driftingGratings":
            taskData = [behaviorData, self.taskParameters]
            taskData = pd.concat(taskData, axis = 1, join = 'outer')
        else:
            taskData = behaviorData
        
        # Save experiment data
        fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "behavior" + "_" + str(self.blockID)
        if behaviorData.empty:
            print("DataFrame is empty. Most likely an experiment has not been run yet.")
        else:
            if not os.path.isfile(fileName + self.fileExtension):
                taskData.to_pickle(fileName + self.fileExtension)
                messagebox.showinfo("Data Saved", "Experiment data have been saved at " + self.pathForSavingData)
            else:
                isNotSaved = True
                while isNotSaved is True:
                    blockID = fileName[-1]
                    blockID = int(blockID)
                    blockID += 1
                    fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + "behavior" + "_" + str(blockID)
                    if not os.path.isfile(fileName + self.fileExtension):
                        taskData.to_pickle(fileName + self.fileExtension)
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
            
            
"""
Main Block

"""

if __name__ == "__main__":
    mazeGUI = mazeGUI.__init__()