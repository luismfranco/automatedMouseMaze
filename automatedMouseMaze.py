"""
Modules

"""

import sys; sys.path.append("src")
import json
import tkinter as tk
from tkinter import messagebox
import mazeGUI


"""
Configuration

"""

f = open("config/package.json")
configurationData = json.load(f)
f.close()

try:
    f = open("config/emailSettings.json")
    emailSettings = json.load(f)
    f.close()
except:
    messagebox.showwarning("Email Settings", "If you would like to receive maze notifications,"
                           "\n " +
                           "\nplease configure an email address and server.")
    emailSettings = None


""" 
Run Application

"""

mainWindow = tk.Tk()
mazeGUI.mazeGUI(mainWindow, configurationData, emailSettings)
mainWindow.mainloop()