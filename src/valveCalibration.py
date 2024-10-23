"""
Modules

"""

import tkinter as tk
from tkinter import font as tkFont
import time

"""
Valve calibration

"""

class valveCalibration:
    
    def __init__(self, calibrationWindow, board, waterPorts):
    
        # Create a new window
        self.valveWindow = calibrationWindow
        self.valveWindow.title('Valve Calibration')
        windowWidth = 300
        windowHeight = 200
        screenWidth = self.valveWindow.winfo_screenwidth()
        screenHeight = self.valveWindow.winfo_screenheight()
        x = (screenWidth/2) - (windowWidth/2)
        y = (screenHeight/2) - (windowHeight/2)
        self.valveWindow.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.backGroundColor = self.valveWindow.cget('bg')
        buttonFont = tkFont.Font(family = 'helvetica', size = 12)
        
        # Frames
        frame1 = tk.Frame(self.valveWindow, width = 300, height = 150)
        frame1.place(anchor = "c", relx = 0.5, rely = 0.3)
        frame2 = tk.Frame(self.valveWindow, width = 300, height = 50)
        frame2.place(anchor = "c", relx = 0.5, rely = 0.8)
        
        # Parameters labels
        tk.Label(frame1, font = buttonFont, text = "Calibration Parameters", width = 12, anchor  = 'c').grid(row = 0, column = 0, columnspan = 3 , padx = 10, pady = 10, sticky = 'we')
        entryLabels = ["time","frequency","repetitions"]
        entryLabelsUnits = ["ms","Hz"," "]
        nrow = 1
        for i in range(len(entryLabels)):
            tk.Label(frame1, font = buttonFont, text = entryLabels[i], width = 8, anchor  = 'e').grid(row = nrow, column = 0, padx = 10)
            tk.Label(frame1, font = buttonFont, text = entryLabelsUnits[i], width = 8, anchor  = 'w').grid(row = nrow, column = 2, padx = 10)
            nrow += 1
        
        # Water ports
        self.board = board
        self.leftWaterPort = waterPorts[0]
        self.rightWaterPort = waterPorts[1]
        
        # Valve open time
        self.openTime = 100 # in ms
        self.openTimeEntry = tk.Entry(frame1, font = 8, width = 10)
        self.openTimeEntry.insert(0, self.openTime)
        self.openTimeEntry.grid(row = 1, column = 1, sticky ='w')
        
        # Frequency
        self.frequency = 5 # times per second
        self.frequencyEntry = tk.Entry(frame1, font = 8, width = 10)
        self.frequencyEntry.insert(0, self.frequency)
        self.frequencyEntry.grid(row = 2, column = 1, sticky ='w')
        
        # Repetitions
        self.repetitions = 10 # total repetitions
        self.repetitionsEntry = tk.Entry(frame1, font = 8, width = 10)
        self.repetitionsEntry.insert(0, self.repetitions)
        self.repetitionsEntry.grid(row = 3, column = 1, sticky ='w')
        
        # Start button
        self.startButton = tk.Button(frame2, text = 'Start', font = buttonFont, width = 12, command = self.runCalibration)
        self.startButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'we')
        self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Black', bg ='#99D492'))
        self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Black', bg ='SystemButtonFace'))
        
    def updateCalibrationParameters(self):
        
        # Input calibration parameters
        self.openTime = int(self.openTimeEntry.get())
        self.frequency = int(self.frequencyEntry.get())
        self.repetitions = int(self.repetitionsEntry.get())
        
    def closeValves(self):
        
        self.board.digital[self.leftWaterPort].write(0)
        self.board.digital[self.rightWaterPort].write(0)

    def openValves(self):
        
        self.board.digital[self.leftWaterPort].write(1)
        self.board.digital[self.rightWaterPort].write(1)
        
    def runCalibration(self):
        
        # Update calibration parameters
        self.updateCalibrationParameters()
        
        # Run calibration
        if self.openTime * self.frequency >= 1000:
            print("Error: incompatible time and frequency. Try reducing the frequency.")
        else:
            # Update startButton: task is running...
            self.startButton.config(fg = 'Blue', bg = '#99D492', relief = 'sunken', text = 'Running...')
            self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Blue', bg ='#99D492'))
            self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Blue', bg = '#99D492'))
            self.startButton.update_idletasks()
        
            # Run calibration protocol
            openTime = self.openTime/1000
            interTrialInterval = ((1000/self.frequency) - (self.openTime)) / 1000
            
            for i in range(self.repetitions):
                self.openValves()
                time.sleep(openTime)
                self.closeValves()
                time.sleep(interTrialInterval)
        
            # Reset GUI buttons
            self.startButton.config(fg = 'Black', bg = self.backGroundColor, relief = 'raised', text = 'Start')
            self.startButton.bind('<Enter>', lambda e: self.startButton.config(fg = 'Black', bg ='#99D492'))
            self.startButton.bind('<Leave>', lambda e: self.startButton.config(fg = 'Black', bg ='SystemButtonFace'))
            self.startButton.update_idletasks()