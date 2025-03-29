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
<img width="1025" height="500" src="assets/mazeGUI.png">
</p>

However, this app requires a connection with a Teensy board in order to work. Also, the automated maze has several other components, such as IR sensors, solenoid valves, a speaker, and LEDs. To build your own maze, follow this tutorial: 
[maze construction](docs/howToBuildYourOwnMaze.md).

This apps also controls and triggers the recording of video, IMU sensors, and electrophysiology probes. Please refer to Parker et al., 2022 (https://doi.org/10.1016/j.neuron.2022.08.029) for more details on this.

# Configuration settings

Before running your first experiment, make sure your Teensy board is properly [configured](config/package.json):
1. Under ``teensyConfiguration``, select the correct serial ``port`` for communication between the computer and Teensy (e.g. ***COM3***).
2. Under ``stimulusScreen``, select the correct ``screenNumber``. In Windows, you can verify the screen number in: ``Display settings > Display > Identify``.
3. There are also a number of input and output digintal pins under ``teensyConfiguration``. Make sure they are properly assigned according to your electronic circuit (see example below).

### Example board with connections for Teensy pins:

1. Solenoid valves, including transistors and diodes. The solenoids for the maze doors (green wires) require a 24 V power supply. The solenoids for the water rewards (blue wires) require a 12 V power supply. **Important: use diodes to make sure current doesn't flow back from solenoids to Teensy**. In this example, the configuration is:  
   ``"leftStartDoor": "5"``  
   ``"rightStartDoor": "7"``  
   ``"leftDecisionDoor": "9"``  
   ``"rightDecisionDoor": "11"``  
   ``"leftWaterPort": "1"``  
   ``"rightWaterPort": "3"``  
2. IR sensors, including a connection between their white signal wire and the 5V power supply (see the bottom view of the circuit below). In this example, the configuration is:  
   ``"leftStartIRsensor": "22"``  
   ``"rightStartIRsensor": "20"``  
   ``"leftDecisionIRsensor": "18"``  
   ``"rightDecisionIRsensor": "16"``  
   ``"startStimulusIRsensor": "15"``  
   ``"stopStimulusIRsensor": "14"``  
3. LEDs, including transitors diodes and resistors. LEDs require a 5 V power supply. In this example, the configuration is:  
   ``"leftLED": "0"``  
   ``"rightLED": "2"``  

<p align="center">
<img width="800" height="275" src="assets/circuitTopView.png">
</p>
<p align="center">
<img width="800" height="275" src="assets/circuitBottomView.png">
</p>

# How to run this app

In the Command Prompt, activate your environment. Example:  
``conda activate automatedMouseMaze``  
Then, cd to the location where this app was installed, and then type:  
``python automatedMouseMaze.py``

You could also create a batch file. Example:  
``call activate automatedMouseMaze``  
``cd C:\Users\Niell Lab\Documents\automatedMouseMaze\Application\``  
``python automatedMouseMaze.py``  

# Before running an experiment

Under ``task``, please select ``valveCalibration`` and click on ``Initialize Task``. This will open a small window with three parameters:

<p align="center">
<img width="300" height="230" src="assets/valveCalibrationGUI.png">
</p>

1. ``time`` for the opening water valves (in ms).
2. ``frequency`` for valve openning repetitions (in Hz). Make sure ``frequency`` is slow enough to allow the full openning ``time`` in each repetition.
3. Number of ``repetitions``. The shorter the ``time`` the more ``repetitions`` are needed to minimize measurement errors.

Example parameters for a calibration curve are displayed in the terminal every time ``valveCalibration`` is initialized:  
``Time:           5,  10,  15,  20,  25,  30,  40,  50,  60,  80, 100``  
``Frequency:     25,  25,  20,  15,  15,  15,  10,  10,   5,   5,   5``  
``Repetitions: 1500, 750, 500, 400, 300, 250, 200, 150, 125, 100,  50``  

Once you have calculated the correct valve opening time for 5, 6, 7, 8, 9 and 10 μL, you can update the ``src/mazeGUI.py`` script in the "Reward" subsection of the ``__init__`` method in the  ``class mazeGUI``:  
``self.estimatedReward = 0``  
``self.leftRewardStreak = [32, 36, 41, 45, 49, 54] # in ms``  
``self.rightRewardStreak = [32, 37, 41, 46, 50, 55] # in ms``  
``self.rewardAmounts = [ 5,  6,  7,  8,  9, 10] # in μL``  

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

Once your have selected your desired options, you can click on ``Initialize Task``. This will establish a connection between the computer and Teensy. It will also initialize the visual stimulus in the background, but it will not show it yet. Clicking on ``Initialize Task`` disables all fields in the "Task Parameters" and "Experiment Data" boxes. If you would like to change something, click on ``Cancel Task``. This will allow you to access all fields again, but you will need to ``Initialize Task`` again afterwards.

Next, clikc on ``Start Task`` to start running your experiment. If you would like to record video and do electrophysiology as well (see below), make sure you have initialized those options before clickin on ``Start Task``. After a task has started, only the door selected in ``start door`` (see above) will open, and the visual stimulus will be displayed on the screen throughout the trial, unless the on and/or off switchs are enabled (see above).

If you would like to stop the task prematurely (i.e., before reaching the maximum trial number or the maximum duration), click on ``End Task``.

At the end of each experiment, if ``auto save`` is enabled, data are automatically saved. Also, if ``auto save`` is not enabled, or in case of an unexepcted crash (and if the GUI is still available), you can click on ``Save Data`` to manually save your experiment data.

To close the app GUI, click on ``Close`` or on the upper right "X".

# Camera Controls

1. ``Start Cameras`` opens a preview window for the eye and the world cameras, which record the movement of one eye of the mouse and the world in front of its head, respectively. This preview also creates temporary files in the ``path`` for saving data. Data will only be permanently saved if the ``Record Video`` button is pressed.
2. ``Record Video`` starts the recording of video from both the eye and the world cameras.
3. ``Stop recording`` stops the recording of video in both cameras.
4. ``Close Cameras`` closes the preview window.

***Important: make sure you start your video recordings before starting your task to avoid losing data***

# Electrophysiology and IMU Controls

- under development...

# Task

As mentioned above, the option ``task`` allows you to select between 4 different built-in tasks:

1. Drifting gratings (based on Psychopy [https://github.com/psychopy/psychopy]).
2. Motion selectivity (based on Psychopy [https://github.com/psychopy/psychopy]).
3. White noise (based on OpenCV https://github.com/opencv/opencv).
4. Object discrimination (based on Pygame [https://github.com/pygame/pygame], and on ModernGL [https://github.com/moderngl/moderngl]).
5. There is also another option for calibrating your solenoid valves (see section above).

It is easy to change the settings for the [drifting gratings](src/driftingGratings.py), [motion selectivity](src/motionSelectivity.py) and [white noise](src/whiteNoise.py) tasks under their respective ``initializeStimulus`` and ``startStimulus`` methods. Please refer to Psychopy documentation to learn more about the available options for [GratingStim](https://www.psychopy.org/api/visual/gratingstim.html) and [DotStim](https://www.psychopy.org/api/visual/dotstim.html).

# While task is running

The app GUI displays general maze parameters and behavior stats on the left-hand side that continuously update through the experiemntal session.

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


