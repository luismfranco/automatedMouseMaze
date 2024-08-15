# automatedMouseMaze (under development)

GUI for behavioral and neurophysiological experiments in an automated maze for in mice  
Currently under development in the Niell Lab (https://nielllab.uoregon.edu/)

***Important: this app is currently under development***

***Disclamimer: the initial designs for this automated maze were based on experiments currently done in the Sylwestrak Lab*** (https://www.sylwestraklab.com/)

# Installation

### Requirements:
1. Operating System: Windows
2. Anaconda (https://www.anaconda.com/)

### Step by step:
In the Command Prompt:
1. Create your environment. Example:  
``conda create -n "automatedMouseMaze" python=3.10.14 pip``
2. Choose a location where you would like to copy this repo. Example:  
``cd C:\Users\<yourUser>\Documents\automatedMouseMaze\Application\``
3. Clone this repository:  
``git clone https://github.com/luismfranco/automatedMouseMaze.git``
4. Install dependencies:  
``pip install .``
5. This code was developed for Python - Teensy 4.0 communication. pyfirmata was developed for Arduino. There is bug in pyfirmata when trying to input the Teensy 4.0 layout. To fix it, run:  
``python debugPyFirmata`` 

# How to run it
In the Command Prompt, cd to the location where this app was installed, and then type:  
``python mazeGUI.py``

Or, create a batch file:  
``add this later``


<p align="center">
<img width="800" height="450" src="assets/mazeGUI.png">
</p>

