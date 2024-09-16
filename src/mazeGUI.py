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

# Teensy modules
import pyfirmata
import serial
import serial.tools.list_ports
import simpleaudio as sa

# Visual stimulus module
import driftingGratings
import objectDiscrimination

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
    
    def __init__(self,mainWindow,configurationData):
        
        
        """
        GUI Layout
        
        """
        
        # Geometry
        self.mainWindow = mainWindow
        self.mainWindow.title('Automated Mouse Maze')
        windowWidth = 800
        windowHeight = 450
        screenWidth = self.mainWindow.winfo_screenwidth()
        screenHeight = self.mainWindow.winfo_screenheight()
        x = (screenWidth/2) - (windowWidth/2)
        y = (screenHeight/2) - (windowHeight/2)
        self.mainWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.backGroundColor = self.mainWindow.cget('bg')
        buttonFont = tkFont.Font(family = 'helvetica', size = 12)
        
        # Frames
        frame1 = tk.Frame(self.mainWindow, width = 250, height = 500)
        frame1.grid(row = 0, rowspan = 3, column = 0, sticky = 'news')
        frame11 = tk.Frame(frame1, width = 250, height = 200)
        frame11.place(anchor = "c", relx = 0.5, rely = 0.2)
        frame12 = tk.Frame(frame1, width = 250, height = 250)
        frame12.place(anchor = "c", relx = 0.5, rely = 0.6)
        frame2 = tk.Frame(self.mainWindow, width = 550, height = 350)
        frame2.grid(row = 0, rowspan = 2, column = 1, sticky = 'news')
        frame21 = tk.Frame(frame2, width = 550, height = 150)
        frame21.grid(row = 0, column = 0)
        frame22 = tk.Frame(frame2, width = 550, height = 150)
        frame22.grid(row = 1, column = 0)
        frame3 = tk.Frame(self.mainWindow, width = 550, height = 150)
        frame3.grid(row = 2, column = 1, sticky = 'news')
        frame31 = tk.Frame(frame3, width = 550, height = 150)
        frame31.place(anchor = "c", relx = 0.5, rely = 0.35)
        
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
        
        # Door labels
        tk.Label(frame11, font = buttonFont, text = "Doors", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3 , padx = 10, pady = 10, sticky = 'we')
        labelList = ["start left","start right","decision left","decision right"]
        nrow = 1
        for i in range(len(labelList)):
            tk.Label(frame11, font = buttonFont, text = labelList[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
            
        # Maze state
        self.mazeState = 0
            
        # Door states
        self.leftStartLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.leftStartLabel.grid(row = 1, column = 1)
        self.rightStartLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.rightStartLabel.grid(row = 2, column = 1)
        self.leftDecisionLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.leftDecisionLabel.grid(row = 3, column = 1)
        self.rightDecisionLabel = tk.Label(frame11, bg = '#99D492', font = buttonFont, text = "open", width = 8)
        self.rightDecisionLabel.grid(row = 4, column = 1)
        
        # IR sensor values
        self.leftStartValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.leftStartValue.grid(row = 1, column = 2)
        self.rightStartValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.rightStartValue.grid(row = 2, column = 2)
        self.leftDecisionValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.leftDecisionValue.grid(row = 3, column = 2)
        self.rightDecisionValue = tk.Label(frame11, font = buttonFont, text = 0)
        self.rightDecisionValue.grid(row = 4, column = 2)
        
        
        """
        Task Parameters
        
        """
        
        # Parameters labels
        tk.Label(frame22, font = buttonFont, text = "Task Parameters", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 4 , padx = 10, pady = 10, sticky = 'we')
        entryLabels0 = ["trials","duration","task","startDoor","cues"]
        entryLabels2 = ["rig","animal","path","autoSave"," "]
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
        self.taskList = ["driftingGratings","objectDiscrimination"]
        self.taskName = " "
        self.taskBox = ttk.Combobox(frame22, width = 12, font = 8, state = 'readonly', values = self.taskList)
        self.taskBox.grid(row = 3, column = 1, sticky ='w')
        
        # Animal start list
        self.startList = ["left","right"]   # 0 = left, 1 = right
        self.startBox = ttk.Combobox(frame22, width = 12, font = 8, state = 'readonly', values = self.startList)
        self.startBox.current(0)
        self.startBox.grid(row = 4, column = 1, sticky ='w')
        
        # Cues checkBox
        self.useTrialCues = tk.BooleanVar(value = True)
        cuesBox = tk.Checkbutton(frame22, text = "sounds + LEDs", font = 8, variable = self.useTrialCues, onvalue = True, offvalue = False)
        cuesBox.grid(row = 5, column = 1, sticky = 'w')

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
        self.animalEntry.grid(row = 2, column = 3, sticky='w')
        
        # Path entry
        userName = os.getlogin()
        self.currentDate = datetime.today().strftime("%y%m%d")
        self.pathForSavingData = "C:\\Users\\" + userName + "\\Documents\\automatedMouseMaze\\Data\\" + self.currentDate + "\\"
        self.pathEntry = tk.Entry(frame22, font = 8, width = 14)
        self.pathEntry.insert(0, self.pathForSavingData)
        self.pathEntry.grid(row = 3, column = 3, sticky ='w')
        
        # AutoSave checkBox
        self.autoSaveData = tk.BooleanVar(value = True)
        autoSaveBox = tk.Checkbutton(frame22, text = "save to path", font = 8, variable = self.autoSaveData, onvalue = True, offvalue = False)
        autoSaveBox.grid(row = 4, column = 3, sticky = 'w')
        
        
        """
        Behavior Stats
        
        """
        
        # Stats labels
        tk.Label(frame12, font = buttonFont, text = "Behavior", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3 , padx = 10, pady = 10, sticky = 'we')
        labelList = ["performance","bias index","correct","incorrect","left decisions","right decisions", "reward (μL)"]
        nrow = 1
        for i in range(len(labelList)):
            tk.Label(frame12, font = buttonFont, text = labelList[i], width = 12, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            nrow += 1
            
        # Behavior parameters
        self.performance = 0
        self.biasIndex = 0
        self.correct = 0
        self.incorrect = 0
        self.left = 0
        self.right = 0
        
        # Reward
        self.estimatedReward = 0
        self.rewardStreak = [22, 24, 26, 29, 31, 34] # in ms
        self.rewardAmounts = [ 5,  6,  7,  8,  9, 10] # in μL
        
        # Behavior values in GUI
        self.performanceValue = tk.Label(frame12, font = buttonFont, text = self.performance)
        self.performanceValue.grid(row = 1, column = 1)
        self.biasIndexValue = tk.Label(frame12, font = buttonFont, text = self.biasIndex)
        self.biasIndexValue.grid(row = 2, column = 1)
        self.correctValue = tk.Label(frame12, font = buttonFont, text = self.correct)
        self.correctValue.grid(row = 3, column = 1)
        self.incorrectValue = tk.Label(frame12, font = buttonFont, text = self.incorrect)
        self.incorrectValue.grid(row = 4, column = 1)
        self.leftValue = tk.Label(frame12, font = buttonFont, text = self.left)
        self.leftValue.grid(row = 5, column = 1)
        self.rightValue = tk.Label(frame12, font = buttonFont, text = self.right)
        self.rightValue.grid(row = 6, column = 1)
        self.rewardValue = tk.Label(frame12, font = buttonFont, text = self.estimatedReward)
        self.rewardValue.grid(row = 7, column = 1)
        
        
        """
        Task Control Buttons
        
        """
        
        # Ready button
        self.readyButton = tk.Button(frame31, text = 'Initialize', font = buttonFont, width = 12, command = self.readyTask)
        self.readyButton.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Black', bg ='#A9C6E3'))
        self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
        # Cancel button
        self.cancelButton = tk.Button(frame31, text = 'Cancel', font = buttonFont, width = 12, command = self.cancelTask)
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
        
        # Water ports
        self.leftWaterPort = int(configurationData["teensyConfiguration"]["leftWaterPort"])
        self.rightWaterPort = int(configurationData["teensyConfiguration"]["rightWaterPort"])
    
        # Check available serial ports
        availableSerialPorts = serial.tools.list_ports.comports()
        portIDs = []
        for port, desc, hwid in sorted(availableSerialPorts):
            portIDs.append(port[3])
        
        if not self.port[3] in portIDs:
            self.closeGUIWithoutCheckouts = True
            messagebox.showinfo("Error", "Make sure the serial port for Teensy 4.0 in 'config/package.json' is correct before initializing maze.")
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
                doorNames = [self.leftStartDoor,self.rightStartDoor,self.leftDecisionDoor,self.rightDecisionDoor]
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
            self.board.digital[self.leftDecisionDoor].write(1)
            self.board.digital[self.rightDecisionDoor].write(1)
            self.leftDecisionLabel.config(bg = 'pink', text = "closed")
            self.rightDecisionLabel.config(bg = 'pink', text = "closed")
            
        # Mouse coming from the left
        elif self.mazeState == 3:
            self.board.digital[self.leftStartDoor].write(0)
            self.leftStartLabel.config(bg = '#99D492', text = "open")
            
        # Mouse coming from the right
        elif self.mazeState == 4:
            self.board.digital[self.rightStartDoor].write(0)
            self.rightStartLabel.config(bg = '#99D492', text = "open")
    
    def readPinStates(self):
        
        # Read pins
        self.LD = self.board.digital[self.leftDecisionIRsensor].read()
        self.RD = self.board.digital[self.rightDecisionIRsensor].read()
        self.LS = self.board.digital[self.leftStartIRsensor].read()
        self.RS = self.board.digital[self.rightStartIRsensor].read()
        
        # Update door values in GUI
        doorLabelValues = [self.leftStartValue,self.rightStartValue,self.leftDecisionValue,self.rightDecisionValue]
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
            currentTime = time.time()
            if currentTime > self.interTrialStart + self.interTrialTimeOut:
                if self.startDoor == "left":
                    self.mazeState = 3
                elif self.startDoor == "right":
                    self.mazeState = 4
        elif self.mazeState == 3 or self.mazeState == 4:
            if self.LS is False or self.RS is False:
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
                self.reward = False

    def giveReward(self):
        
        if self.reward is False:
            if self.targetLocation == 0:
                self.waterPort = self.leftWaterPort
            elif self.targetLocation == 1:
                self.waterPort = self.rightWaterPort
            self.reward = True
            self.estimatedReward = self.estimatedReward + self.rewardSize
            self.board.digital[self.waterPort].write(1)
            self.rewardStart = time.time()


    """ 
    Task Functions
    
    """
    
    def initializeTaskParameters(self):
        
        # Task
        self.trialID = 0
        self.runningTask = False
        self.interTrialTimeOut = 3          # possibly add more time out for incorrect trials
        self.probabilityTargetLeft = 0.5
        
        # Behavior stats
        self.performance = 0
        self.biasIndex = 0
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
        self.dataFrameStartTime = []
        self.dataFrameEndTime = []
    
    def updateTrialParameters(self):
        
        # Input task parameters
        self.maximumTrialNumber = int(self.trialsEntry.get())
        self.timeout = int(self.timeEntry.get())
        self.taskName = str(self.taskBox.get())
        self.startDoor = str(self.startBox.get())
        self.trialCues = bool(self.useTrialCues.get())
        self.animalID = str(self.animalEntry.get())
        self.rigID = str(self.rigEntry.get())
        self.autoSave = bool(self.autoSaveData.get())
        
    def readyTask(self):
        
        # Prepare directory to save data
        Path(self.pathForSavingData).mkdir(parents = True, exist_ok = True)
        
        # Update task parameters
        self.updateTrialParameters()
        
        # Flush all data from previous task
        self.initializeTaskParameters()
        
        # Display task parameters when initializing task
        print(" ")
        print("     Task Parameters:")
        print("          Task name:",self.taskName)
        print("          Maximum number of trials:",self.maximumTrialNumber)
        print("          Maximum session time (s):",self.timeout)
        print("          Start door:",self.startDoor)
        print("          Use sound cues:",str(self.trialCues).lower())
        print("          Animal ID:",self.animalID)
        print("          Rig ID:",self.rigID)
        print("          AutoSave:",self.autoSave)
        print(" ")
        
        # Initialize connection with Teensy 4.0
        if not self.taskName in self.taskList:
            messagebox.showinfo("Error", "Please select a task before initializing maze.")
        else:
            # Update startButton: connecting to board...
            self.readyButton.config(fg = 'Black', bg = '#A9C6E3', text = 'Connecting...', relief = 'sunken')
            self.readyButton.update_idletasks()
            # Connect to board
            self.connectToTeensy()
            # Update startButton: task is running...
            self.readyButton.config(fg = 'Blue', bg = '#A9C6E3', relief = 'sunken', text = 'Ready')
            self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Blue', bg ='#99D492'))
            self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Blue', bg = '#99D492'))
            self.readyButton.update_idletasks()
            # Update maze
            self. mazeState = 0
            self.updateDoors()
            
        # Initialize visual stimulus
        if self.taskName == "driftingGratings":
            self.visualStimulus = driftingGratings.driftingGratings()
        elif self.taskName == "objectDiscrimination":
            self.visualStimulus = objectDiscrimination.objectDiscrimination()
            
    def cancelTask(self):
        
        boardAvailable = self.checkIfPortAvailable()
        if boardAvailable is False:
            self.resetTask()
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
            # Disconnect Teensy board
            self.disconnectFromTeensy()
            # Reset GUI buttons
            self.startButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start')
            self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Black', bg ='#99D492'))
            self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.readyButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Initialize')
            self.readyButton.bind('<Enter>', lambda e: self.readyButton.config(fg = 'Black', bg ='#A9C6E3'))
            self.readyButton.bind('<Leave>', lambda e: self.readyButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.readyButton.update_idletasks()
        
        # Close visual stimulus window
        self.visualStimulus.closeWindow()
        
        # Save experiment data
        if self.autoSave is True:
            self.saveData()
            
    def startTrial(self):
        
        # Set up current trial
        self.targetLocation = np.random.choice([0,1], p = [1-self.probabilityTargetLeft, self.probabilityTargetLeft])
        
        # Reward streak
        if self.correctStreak < len(self.rewardStreak):
            self.rewardTime = self.rewardStreak[self.correctStreak] / 1000 # in ms
            self.rewardSize = self.rewardAmounts[self.correctStreak] # in μL
        else:
            self.rewardTime = self.rewardStreak[-1] / 1000 # in ms
            self.rewardSize = self.rewardAmounts[-1] # in μL
        
        # Display trial info in terminal
        self.trialID += 1
        print("     Trial ", self.trialID," started...", " Target -> ", self.targetLocation)
        
        # Display visual stimulus
        self.visualStimulus.startStimulus(display = True, target = self.targetLocation)
            
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
        
        # Bias correction and recent quick stats
        if self.trialID >= 10:
            recentDecisions = self.dataFrameDecision[-10:]
            self.recentBiasIndex = (recentDecisions.count(0) - recentDecisions.count(1)) / len(recentDecisions)
            self.probabilityTargetLeft = 0.5 + (self.recentBiasIndex/2)
            recentCorrect = self.dataFrameCorrect[-10:]
            self.recentPerformance = recentCorrect.count(1) / len(recentCorrect)
        
        # Update behavior stats
        behaviorStats = [self.performance,self.biasIndex,self.correct,self.incorrect,self.left,self.right,self.estimatedReward]
        behaviorValues = [self.performanceValue,self.biasIndexValue,self.correctValue,self.incorrectValue,self.leftValue,self.rightValue,self.rewardValue]
        for i in range(len(behaviorValues)):
            behaviorValues[i].config(text = behaviorStats[i])
            behaviorValues[i].update_idletasks()
        
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
        
        # End task after last trial
        if self.trialID == self.maximumTrialNumber:
            self.runningTask = False
            print(" ")
            print("The task has reached the maximum number of trials!")
        
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
                self.trialType = 1
                self.lastDecision = 0
                self.correctStreak += 1
            elif self.targetLocation == 1:
                self.incorrect += 1
                # Incorrect left
                if self.trialCues is True:
                    sa.play_buffer(self.incorrectSound, 1, 2, self.Fs)
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
                self.trialType = 3
                self.lastDecision = 1
                self.correctStreak = 0
            elif self.targetLocation == 1:
                self.correct += 1
                # Correct right
                self.giveReward()
                if self.trialCues is True:
                    sa.play_buffer(self.correctSound, 1, 2, self.Fs)
                self.trialType = 4
                self.lastDecision = 1
                self.correctStreak += 1
                    
        # Quick stats
        self.performance = round(self.correct / (self.correct + self.incorrect),2)
        self.biasIndex = round((self.left-self.right) / (self.left+self.right),2)
        
    def runTask(self):
        
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
        self.interTrialStart = time.time()
        print(" ")
        
        # Start task
        self.currentRunningTask = Thread(target = self.checkTask())
        self.currentRunningTask.start()
        self.resetTask()
    
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
                "target": self.dataFrameTarget,
                "decision": self.dataFrameDecision,
                "correct": self.dataFrameCorrect,
                "trial type": self.dataFrameTrialType,
                "startTime": self.dataFrameStartTime,
                "endTime": self.dataFrameEndTime,
                                                      }
        df = pd.DataFrame.from_dict(data, orient = 'index')
        df = df.transpose()
        
        # Save experiment data
        blockID = 1
        fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + str(blockID)
        if df.empty:
            print("DataFrame is empty. Most likely an experiment has not been run yet.")
        else:
            if not os.path.isfile(fileName + self.fileExtension):
                df.to_pickle(fileName + self.fileExtension)
            else:
                isNotSaved = True
                while isNotSaved is True:
                    blockID = fileName[-1]
                    blockID = int(blockID)
                    blockID += 1
                    fileName = self.pathForSavingData + self.animalID + "_" + self.currentDate + "_" + str(blockID)
                    if not os.path.isfile(fileName + self.fileExtension):
                        df.to_pickle(fileName + self.fileExtension)
                        
                        isNotSaved = False
            print("Experiment data have been saved successfully.")
            print(" ")
            messagebox.showinfo("Data Saved", "Experiment data have been saved at " + self.pathForSavingData)
        
    def closeMainWindow(self):
        
        # Kill GUI
        boardAvailable = self.checkIfPortAvailable()
        if boardAvailable is False and self.closeGUIWithoutCheckouts is False:
            print("Please click on 'End Task' before closing this program.")
        elif boardAvailable is True or self.closeGUIWithoutCheckouts is True:
            self.mainWindow.destroy()
            self.mainWindow.quit()