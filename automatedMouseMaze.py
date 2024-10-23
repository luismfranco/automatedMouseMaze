"""
Modules

"""

import sys; sys.path.append("src")
import json
import tkinter as tk
import mazeGUI

"""
Configuration

"""

f = open("config/package.json")
configurationData = json.load(f)
f.close()

""" 
Run Application

"""

mainWindow = tk.Tk()
mazeGUI.mazeGUI(mainWindow, configurationData)
mainWindow.mainloop()