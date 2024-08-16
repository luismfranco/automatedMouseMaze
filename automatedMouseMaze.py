import json
import tkinter as tk
import mazeGUI

f = open("config/package.json")
configurationData = json.load(f)
f.close()

mainWindow = tk.Tk()
mazeGUI.mazeGUI(mainWindow,configurationData)
mainWindow.mainloop()
