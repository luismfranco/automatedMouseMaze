# automatedMouseMaze (under development)

GUI for behavioral and neurophysiological experiments in an automated maze for in mice.
Currently under development in the Niell Lab (https://nielllab.uoregon.edu/).

***Important: this app is currently under development***

***Disclamimer: the initial designs for this automated maze are based on previous work done at the Sylwestrak Lab*** (https://www.sylwestraklab.com/)

# Installation

### Requirements:
1. Operating System: Windows.
2. Anaconda (https://www.anaconda.com/).
3. Microsoft Visual C++ 14.0 or greater (https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### Step by step:
In the Command Prompt:
1. Create your environment. Example:  
``conda create -n automatedMouseMaze python=3.10.14 pip``
2. Activate your environment:  
``conda activate automatedMouseMaze``
3. Choose a location where you would like to copy this repo. Example:  
``mkdir Documents\automatedMouseMaze\Application``  
``cd Documents\automatedMouseMaze\Application\``
4. Clone this repository:  
``git clone https://github.com/luismfranco/automatedMouseMaze.git .``
5. Install dependencies in your environment:  
``pip install .``
6. This code was developed for Python - Teensy 4.0 communication. pyfirmata was developed for Arduino. There is bug in pyfirmata when trying to input the Teensy 4.0 layout. To fix it, run:  
``python src\debugPyFirmata.py`` 

If everything went well, you should be able to run the GUI:  
``python automatedMouseMaze.py``
<p align="center">
<img width="800" height="450" src="assets/mazeGUI.png">
</p>

However, this app requires a connection with a Teensy board in order to work. Also, the automated maze has several other components, such as IR sensors, solenoid valves, a speaker, and LEDs. To build your own maze, follow this tutorial:  
[maze construction](docs/howToBuildYourOwnMaze.md)

# How to run this app
In the Command Prompt, activate your environment. Example:  
``conda activate automatedMouseMaze``  
Then, cd to the location where this app was installed, and then type:  
``python automatedMouseMaze.py``

You could also create a batch file. Example:  
``call activate automatedMouseMaze``  
``cd C:\Users\Niell Lab\Documents\automatedMouseMaze\Application\``  
``python automatedMouseMaze.py``  

# Configuration settings
Make sure your Teensy board is properly [configured](config/package.json).

Under ``teensyConfiguration``, select the correct serial port for communication between the computer and Teensy (e.g. ***COM3***).

There are a number of input and output digintal pins. Make sure there are properly assigned according to your electronic circuit:
<p align="center">
<img width="800" height="450" src="assets/circuitTopView.png">
</p>

Under ``stimulusScreen``, select the correct screen number. In Windows, you can verify the screen number in:
``Display settings > Display > Identify``.

# How to run an experiment

There are a few options you can select before running an experiment, such as:

1. Maximum number of ``trials``.
2. Maximum ``duration`` of the experiment (in seconds).
3. The particular visual stimulus, under ``task`` (more details below).
4. The location of the animal at the start of the session, under ``startDoor``. This is the door that will open for the first trial.
5. Sounds and light ``cues`` for helping during learning of the task.
6. Name of your ``rig``.
7. Name of your ``animal``.
8. ``path`` for saving the experiment data.
9. ``autoSave`` option.

Once your have selected your desired options, you can click on ``Initialize``. This is establish a connection between the computer and Teensy. 
In addition, this will prepare the visual stimulus, and have it ready for display after clicking on ``Start Task``.

# Task

As mentioned above, the option ``task`` allows you to select between 3 different built-in tasks:

1. Drifting gratings (based on Psychopy, https://github.com/psychopy/psychopy)
2. Motion selectivity (based on Psychopy, https://github.com/psychopy/psychopy)
3. Object discrimination (based on Pygame, https://github.com/pygame/pygame, and on ModernGL, https://github.com/moderngl/moderngl)

There is also another option for calibrating your solenoid valves (use for reward delivery).

# What's in the data pickle file?
Describe data fields...









