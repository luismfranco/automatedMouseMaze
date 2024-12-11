"""
Modules

"""

import cv2
import numpy as np
import time
from datetime import datetime
from scipy.fftpack import ifftn, ifftshift


"""
White Noise

"""

class whiteNoise:
    
    def __init__(self, stimulusScreen, screenSize):

        # Get screen dimensions and positions
        self.screenSize = screenSize
        screenWidth = screenSize[0]
        
        # Calculate window position
        x_pos = screenWidth * stimulusScreen
        y_pos = 0
        
        # Create stimulus window
        cv2.namedWindow("whiteNoiseStimulus", cv2.WINDOW_NORMAL)
        cv2.moveWindow("whiteNoiseStimulus", x_pos, y_pos)
        cv2.setWindowProperty("whiteNoiseStimulus",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        self.waitFrame = np.full((128,128), 255)
        self.waitFrame = self.waitFrame.astype(np.uint8)
        cv2.imshow("whiteNoiseStimulus", self.waitFrame)
        
        # Type of stimulus
        self.leftTarget = 'static'
        self.rightTarget = 'dynamic'
        
        # Stimulus
        self.showVisualStimulus = False
        self.stimulusFrameRate = 30     # Hz
        
    def startStimulus(self, **kwargs):
        
        # Start stimulus
        self.showVisualStimulus = kwargs['display']
        self.targetLocation = kwargs['target']
        if self.targetLocation == 0:
            self.target = self.leftTarget
            duration = 2
            whiteNoise = createWhiteNoise(duration, self.screenSize, self.stimulusFrameRate)
        elif self.targetLocation == 1:
            self.target = self.rightTarget
            duration = 15
            whiteNoise = createWhiteNoise(duration, self.screenSize, self.stimulusFrameRate)
            
        # Stimulus
        self.whiteNoiseStimulus = whiteNoise.whiteNoise()
        self.frameNumber = 0
        self.lastFrame = self.whiteNoiseStimulus.shape[2] - 1
        noiseFrame = self.whiteNoiseStimulus[:, :, self.frameNumber]
        cv2.imshow("whiteNoiseStimulus", noiseFrame)
        self.currentFrameTime = time.time()
        
    # Display and update the stimulus
    def updateStimulus(self):
            
        if self.showVisualStimulus is True:
            if self.target == self.rightTarget:
                if time.time() > self.currentFrameTime + (1/self.stimulusFrameRate):
                    self.frameNumber += 1
                    noiseFrame = self.whiteNoiseStimulus[:, :, self.frameNumber]
                    cv2.imshow("whiteNoiseStimulus", noiseFrame)
                    self.currentFrameTime = time.time()
                    if self.lastFrame == self.frameNumber:
                        self.frameNumber = 0
            
    def stopStimulus(self, **kwargs):
        
        self.showVisualStimulus = kwargs['display']
        cv2.imshow("whiteNoiseStimulus", self.waitFrame)
    
    # Cleanup
    def closeWindow(self):
        
        cv2.destroyAllWindows()
        
        
"""
Create White Noise

"""

class createWhiteNoise:
    
    def __init__(self, duration, screenSize, frameRate):

        # Random seed based on the current clock
        currentTime = datetime.now()
        seed = int(sum(100 * np.array([currentTime.hour, currentTime.minute, currentTime.second])))
        np.random.seed(seed)
        
        # Screen properties
        screenWidthPixels = screenSize[0]       # Screen width in pixels
        screenWidthSize = 16.5                  # Width in cm
        screenDistance = 10                     # Distance in cm
        
        # Stimulus parameters
        self.binarize = 0                       # Default value for binarize
        # movtype = 0                           # Default value for movtype
        self.imageSize = 256                    # Size in pixels
        imageMagnification = 9.0                # Magnification
        maximumSpatialFrequency = 0.07          # Spatial frequency cutoff (cpd)
        maximumTemporalFrequency = 0.5          # Temporal frequency cutoff
        self.contrastSigma = 0.5                # One-sigma value for contrast

        # Derived parameters
        screenWidthDegrees = 2 * np.arctan(0.5 * screenWidthSize / screenDistance) * 180 / np.pi
        degreesPerPixel = (screenWidthDegrees / screenWidthPixels) * imageMagnification
        self.nframes = int(frameRate * duration)
        
        # Frequency intervals for FFT
        NyquistInterval = 0.5
        frequencyInterval = NyquistInterval / (0.5 * self.imageSize)
        Nyquist = frameRate / 2
        temporalFrequencyInterval = Nyquist / (0.5 * self.nframes)
        
        # Cutoffs in terms of frequency intervals
        self.temporalCutoff = round(maximumTemporalFrequency / temporalFrequencyInterval)
        maximumFrequency = maximumSpatialFrequency * degreesPerPixel
        self.spatialCutoff = round(maximumFrequency / frequencyInterval)

    def frequencySpectrum(self):

        # Generate frequency spectrum (inverseFFT)
        alpha = -1
        offset = 3
        range_mult = 1
        spaceRange = slice(self.imageSize // 2 - range_mult * self.spatialCutoff, self.imageSize // 2 + range_mult * self.spatialCutoff + 1)
        temporalRange = slice(self.nframes // 2 - range_mult * self.temporalCutoff, self.nframes // 2 + range_mult * self.temporalCutoff + 1)
        x, y, z = np.meshgrid(np.arange(-range_mult * self.spatialCutoff, range_mult * self.spatialCutoff + 1),
                              np.arange(-range_mult * self.spatialCutoff, range_mult * self.spatialCutoff + 1),
                              np.arange(-range_mult * self.temporalCutoff, range_mult * self.temporalCutoff + 1),
                              indexing = "ij")
        
        # Frequency spectrum function
        frequencySpectrum = (((x**2 + y**2) <= (self.spatialCutoff**2)) & (z**2 < self.temporalCutoff**2)).astype(np.float32) * (np.sqrt(x**2 + y**2 + offset) ** alpha)
        
        return spaceRange, temporalRange, frequencySpectrum

    def reconstructImage(self, spaceRange, temporalRange, frequencySpectrum):

        # Initialize the inverse FFT
        inverseFFT = np.zeros((self.imageSize, self.imageSize, self.nframes), dtype = np.complex64)
        mu = np.zeros((spaceRange.stop - spaceRange.start, spaceRange.stop - spaceRange.start, temporalRange.stop - temporalRange.start))
        sig = np.ones_like(mu)
        
        # Assign values to inverseFFT within the defined ranges
        inverseFFT[spaceRange, spaceRange, temporalRange] = (frequencySpectrum * np.random.normal(mu, sig) *
                                                             np.exp(2j * np.pi * np.random.rand(spaceRange.stop - spaceRange.start,
                                                                                                spaceRange.stop - spaceRange.start,
                                                                                                temporalRange.stop - temporalRange.start)))
        del frequencySpectrum, mu, sig, 
        
        # Shift and invert FFT to get real image values
        shiftinverseFFT = ifftshift(inverseFFT)
        rawImage = np.real(ifftn(shiftinverseFFT))
        del inverseFFT, shiftinverseFFT
        
        # Scale the raw image to 0–255 range
        imageMean = np.mean(rawImage)
        imageMax = np.std(rawImage) / self.contrastSigma
        imageMin = -1 * imageMax
        scaledImage = (rawImage - imageMean - imageMin) / (imageMax - imageMin)
        scaledImage = np.clip(scaledImage, 0, 1)                                            # Ensure values are between 0 and 1
        whiteNoiseMovie = np.clip(np.floor(scaledImage * 255), 0, 255).astype(np.uint8)     # Scale to 0-255 range
        
        # Apply binarization if enabled
        if self.binarize:
            scaledImage[scaledImage < 0.5] = 0
            scaledImage[scaledImage >= 0.5] = 1
            
        return whiteNoiseMovie
            
    def whiteNoise(self):
        
        spaceRange, temporalRange, frequencySpectrum = createWhiteNoise.frequencySpectrum(self)
        whiteNoiseMovie = createWhiteNoise.reconstructImage(self, spaceRange, temporalRange, frequencySpectrum)
        
        return whiteNoiseMovie
        