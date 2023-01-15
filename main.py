"""
Module to automate the Chrome Dino game.

1. Open browser.                            DONE
2. Monitor region in front of dinosaur.
    1. invert screen if needed              DONE
	2. find cactus low -> jump and duck     DONE
    3. find bird low -> duck                DONE
3. Detect death
    1. Detect scores.                       TODO
    2. Popup to play again. Reset speed.    TODO
"""

# Standard library imports.
import cv2
import webbrowser
import numpy as np
from mss import mss
import pyautogui as pag
# Local module imports.
from find_objects import findObjects, gameOver
from moves import jump, duck, updateSpeedFactor

# Opening the game online.
webbrowser.open('https://dino-chrome.com/')
# Turning input delay off.
pag.PAUSE = 0
# Bounding boxes for detection.
# BBOX_OBSTACLES = {'top': 610, 'left': 610, 'width': 50, 'height': 80}
BBOX_OBSTACLES = {'top': 530, 'left': 575, 'width': 55, 'height': 160}
BBOX_GAMEOVER = {'top': 610, 'left': 610, 'width': 50, 'height': 80}
BBOX_SCORE = {'top': 610, 'left': 605, 'width': 50, 'height': 80}
# https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
# Loading in default settings for a new game.
DEFAULT_SPEEDFACTOR = 1.5 #1.25
bboxObstacles = BBOX_OBSTACLES.copy()
speedFactor = DEFAULT_SPEEDFACTOR
jumpCntr = 0
sct = mss()

# The main game loop.
while True:
    # Grab the screen.
    imgObstacle = sct.grab(bboxObstacles)
    frame = np.array(imgObstacle)
    cv2.imshow('Q to quit', frame)
    # Make moves.
    obstacles = findObjects(frame)
    if obstacles['top']:
        duck(speedFactor=speedFactor)
        jumpCntr += 1
        print('duck', jumpCntr)
        speedFactor, imgObstacle, bboxObstacles  = updateSpeedFactor(jumpCntr=jumpCntr, 
                                                                     speedFactor=speedFactor, 
                                                                     imgObstacle=imgObstacle,
                                                                     bboxObstacles=bboxObstacles,
                                                                     sct=sct)
    elif obstacles['bottom']:
        jump(speedFactor=speedFactor)
        jumpCntr += 1
        print('jump', jumpCntr)
        speedFactor, imgObstacle, bboxObstacles  = updateSpeedFactor(jumpCntr=jumpCntr, 
                                                                     speedFactor=speedFactor, 
                                                                     imgObstacle=imgObstacle,
                                                                     bboxObstacles=bboxObstacles,
                                                                     sct=sct)       
    # Check if not lost.
    if gameOver(frame):
        speedFactor = DEFAULT_SPEEDFACTOR
        imgScore = sct.grab(BBOX_SCORE)
        # score = np.array(img)
        jumpCntr = 0
    # Check if not closing app.
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        print(DEFAULT_SPEEDFACTOR)
        cv2.destroyAllWindows()
        break