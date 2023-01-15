import pyautogui as pag
import time
import mss

def updateSpeedFactor(jumpCntr: int, speedFactor: float, bboxObstacles: dict, sct: mss.mss,
                      thresh: int = 12, increaseSpeed: float=1.1, increaseBox: int=3
                      ) -> tuple[float, mss.mss, dict[str: int]]:
    """
    Update object detection and input speed depending on the number of taken jumps.

    Parameters
    ----------
    jumpCntr : int
        The number of taken jumps.
    speedFactor : float
        The current speedFactor.
    bboxObstacles : dict
        The current bounding box where OpenCV looks for obstacles.
    sct : mss.mss
        The mss.mss Microsoft ScreenShot object.
    thresh : int, optional
        The number of jumps after which the factors are updated, by default 12.
    increaseSpeed : float, optional
        The relative increase in speed, by default 1.1.
    increaseBox : int, optional
        The absolute rightwards shift of the detection box in pixels, by default 3.

    Returns
    -------
    float
        The updated speedFactor
    mss.mss
        The new detection zone i.e., the mss.mss.grab() object.
    dict[str: int, ...]
        The bounding box of the new detection zone:
        ```dict('top': int, 'bottom': int, 'left': int, 'right': int)```
    """
    speedFactorNew = speedFactor
    if jumpCntr >= thresh:
        if jumpCntr % thresh == 0: #200
            speedFactorNew *= increaseSpeed
            print(f'UPDATING speedFactor: {speedFactor} -> {speedFactorNew}')
        # if jumpCntr % 2*thresh == 0:
            print(f'UPDATING bboxObstacles: {bboxObstacles["left"]} -> {bboxObstacles["left"]+increaseBox}')
            bboxObstacles['left'] += increaseBox
            imgObstacle = sct.grab(bboxObstacles)
    return speedFactorNew, imgObstacle, bboxObstacles

def jump(speedFactor: float=1.0) -> None:
    """Input a jump-and-drop, with airtime depending on speedFactor."""
    pag.press('up')
    time.sleep(0.4 / speedFactor)
    pag.keyDown('down')
    time.sleep(0.12)
    pag.keyUp('down')

def duck(speedFactor: float=1.0) -> None:
    """Input a duck, with groundtime depending on speedFactor."""
    pag.keyDown('down')
    time.sleep(0.4 / speedFactor)
    pag.keyUp('down')