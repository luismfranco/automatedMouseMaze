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
<img width="1025" height="600" src="assets/mazeGUI.png">
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

There are a number of input and output digintal pins. Make sure they are properly assigned according to your electronic circuit:
<p align="center">
<img width="800" height="275" src="assets/circuitTopView.png">
</p>
<p align="center">
<img width="800" height="275" src="assets/circuitBottomView.png">
</p>

Under ``stimulusScreen``, select the correct screen number. In Windows, you can verify the screen number in:  
``Display settings > Display > Identify``.

# How to run an experiment

There are a few options you can select before running an experiment.

Task Parameters:

1. Maximum number of ``trials``.
2. Maximum ``duration`` of the experiment (in seconds).
3. The particular visual stimulus, under ``task`` (more details below).
4. The location of the animal at the start of the session, under ``start door``. This is the door that will open for the first trial.
5. Sounds and light ``cues`` for helping during learning of the task.
6. Triggering the display of the visual ``stimulus`` on the screen.
7. Turning off the display of the visual ``stimulus``.
8. Fraction of trials with ``forced choice``, where only the door for the correct decision is opened. Helpful during early stages of training.

Experiment Data:

1. Name of your ``rig``.
2. Name of your ``animal``.
3. ``block`` number.
4. ``path`` for saving the experiment data.
5. ``autoSave`` option.

Once your have selected your desired options, you can click on ``Initialize``. This will establish a connection between the computer and Teensy. 
In addition, this will prepare the visual stimulus, and have it ready for display after clicking on ``Start Task``.

Camera Controls:

1. ``Start Cameras``.
2. ``Record Video``.
3. ``Stop recording``.
4. ``Close Cameras``.

IMU Controls

- under development...

# Task

As mentioned above, the option ``task`` allows you to select between 3 different built-in tasks:

1. Drifting gratings (based on Psychopy [https://github.com/psychopy/psychopy]).
2. Motion selectivity (based on Psychopy [https://github.com/psychopy/psychopy]).
3. Object discrimination (based on Pygame [https://github.com/pygame/pygame], and on ModernGL [https://github.com/moderngl/moderngl]).
4. There is also another option for calibrating your solenoid valves (used for reward delivery).
<p align="center">
<img width="300" height="230" src="assets/valveCalibrationGUI.png">
</p>

It is easy to change the settings for the [drifting gratings](src/driftingGratings.py) and [motion selectivity](src/motionSelectivity.py) tasks under their respective ``initializeStimulus`` and ``startStimulus`` definitions. Please refer to Psychopy documentation to learn more about the available options for [GratingStim](https://www.psychopy.org/api/visual/gratingstim.html) and [DotStim](https://www.psychopy.org/api/visual/dotstim.html).

# While task is running

Doors:

1. ``maze state``.
2. ``start left``.
3. ``start right``.
4. ``decision left``.
5. ``decision right``.

Stimulus:

1. ``stimulus states``.
2. ``on switch``.
3. ``off switch``.

Behavior:

1. ``performance``.
2.  ``bias index``.
3.  ``alternation index``.
4.  ``trials``.
5.  ``correct``.
6.  ``incorrect``.
7.  ``left decisions``.
8.  ``right decisions``.
9.  ``reward (μL)``.

# Behavior data file

Data are automatically saved at the end of a session in the desired path as a pickle file. This file containa a Pandas DataFrame with the following fields:

1. ``trial`` number.
2. ``startDoor`` for each trial. (0) for left, (1) for right.
3. ``leftTargetProbability`` for each trial. Probability for displaying the target object associated with the left decision.
4. ``target`` object for each trial. (0) for left, (1) for right.
5. animal's ``decision`` for each trial. (0) for left, (1) for right.
6. ``forcedChoice`` for each trial. (0) for no forced choice, (1) for forced correct choice.
7. ``correct`` trial identifier. (0) for incorrect trial, (1) for correct trial.
8. ``trial type``: identifier for correct left (1), incorrect right (2), incorrect left (3), or correct right trials (4).
9. ``startTime``. Time stamp for the start of each trial: opening of start door.
10. ``endTime``. Time stamp for the end of each trial: closing of decision door.
11. ``stimulusStartTime``. Time stamp for the display of the visual stimulus on the screen (if option is enabled).
12. ``stimulusEndTIme``. Time stamp for turning off the display of the visual stimulus (if option is enabled).
13. ``taskRawStartTime``. Time stamp for the start of the task. Important for synchronization with video and electrophysiology recordings.









