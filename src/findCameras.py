"""
Detects and returns a list of available camera IDs.

"""

import cv2

cameraIDrange = 10   # Check a reasonable range of indices

def getCameraIDs():
    
    cameraIDs = []
    for i in range(cameraIDrange):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameraIDs.append(i)
            cap.release()
    return cameraIDs

if __name__ == "__main__":
    availableCameras = getCameraIDs()
    if availableCameras:
        print("Available camera IDs:", availableCameras)
    else:
        print("No cameras found.")
        