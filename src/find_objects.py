import cv2
import numpy as np
from utility import showImage, histogramImage
import matplotlib.pyplot as plt
import pyautogui as pag
from moves import jump, duck


def findObjects(frame: np.ndarray) -> dict['top': bool, 'bottom': bool]:
    """
    Detect obstacles in either the top (bird high/medium) and bottom of the frame (bird low, cacti).

    Parameters
    ----------
    frame: np.ndarray
        The detection zone for obstacles.

    Returns
    -------
    dict['top': bool, 'bottom': bool]:
        Whether (True) or not (False) an obstacle was detected in the respective zone.
    """
    # At least half of the pixels are dark. Frame needs inversion.
    if np.mean(frame) <= frame.max()/2:
        frame = cv2.bitwise_not(frame)
    blur = cv2.GaussianBlur(frame, (5,5), 0)
    # showImage(frame, 'frame')
    # Perform morphological operations to find dark blobs: bird (top) or cactus (bottom).
    _, thresh = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY)
    # showImage(thresh, 'thresh')
    ksize = 5
    kernel = np.ones((ksize,ksize), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    # showImage(closing, 'closing')
    # Split the image in sections and check if these contain any dark pixels.
    top, bottom = np.split(closing, 2, axis=0)
    found = dict(top=False, bottom=False)
    for section, name in zip((top, bottom), found):
        # showImage(section, name)
        found[name] = not np.all(section)
    return found


def gameOver(frame: np.ndarray) -> bool:
    """
    Detect if the game is over.

    Parameters
    ----------
    frame : np.ndarray
        The detection zone for game-over.

    Returns
    -------
    bool
        Whether (True) or not (False) the game is over.
    """
    return False


def readScore(frame: np.ndarray) -> int:
    """
    User OCR to read the score after the game is over.

    Parameters
    ----------
    frame : np.ndarray
        The detection box for the score.

    Returns
    -------
    int
        The detected score.
    """
    return 0


if __name__ == '__main__':
    frame = cv2.imread('./resources/cactus.jpg', cv2.IMREAD_GRAYSCALE)
    objects = findObjects(frame)
    print('regular', objects)

    frame = cv2.imread('./resources/cactus_inverse.jpg', cv2.IMREAD_GRAYSCALE)
    objects = findObjects(frame)
    print('inverse', objects)