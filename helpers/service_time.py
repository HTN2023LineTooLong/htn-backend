from ultralytics import YOLO
from PIL import Image
import glob
import numpy as np
import matplotlib.pyplot as plt
import cv2
from collections import OrderedDict
import time

async def service_time(videoFile):
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO('yolov8n.pt')

    # videoFile was this before: './img/2npc_walkk.mov'
    src = cv2.VideoCapture(videoFile)

    prevBoxCoords = []
    odTracker = OrderedDict()
    counter = 0
    exitCount = 0
    totalServiceTime = 0
    totalPeopleNeeded = 2

    while exitCount < totalPeopleNeeded:
        # Read a frame from the video
        ret, frame = src.read()

        if not ret:
            break

        # Crop the frame to the first 800 pixels of width
        cropped_frame = frame[:, :800]

        # Perform object detection on the cropped frame
        results = model.predict(cropped_frame, classes=0)
        result = results[0]
        boxCoord = (result.boxes.xyxy).numpy()
        
        # SOMEONE ENTERED
        if (len(boxCoord) > len(prevBoxCoords)):
            odTracker[counter] = time.time()   # time is in seconds
            counter += 1
        # SOMEONE LEFT
        elif (len(boxCoord) < len(prevBoxCoords)):
            minIndex = 0
            minValue = prevBoxCoords[0][0]
            for x in range(len(prevBoxCoords)):
                if prevBoxCoords[x][0] < minValue:
                    minValue = prevBoxCoords[x][0]
                    minIndex = x
            
            totalServiceTime += (time.time() - odTracker[minIndex])
            exitCount += 1

        # store previous frame data
        prevBoxCoords = boxCoord

    return totalServiceTime / totalPeopleNeeded