import cv2
import numpy as np
import matplotlib.pyplot as plt

def showImage(img: np.ndarray, windowName: str='image', scaleTo: tuple[int, int]=(1920, 1080)) -> None:
    wImg, hImg = img.shape[:2]
    wScreen, hScreen = scaleTo
    factor = min(wScreen/wImg, hScreen/hImg)
    if factor < 1:
        img = cv2.resize(img, None, fx=factor, fy=factor)
        print(img.shape)
    cv2.imshow(windowName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def histogramImage(image: np.ndarray, channels: list[int]=[0], color:str='k'
                   ) -> tuple[plt.Figure, plt.Axes]:
    """Plot a histogram of an image with at least 1 channel (grayscale).

    Parameters
    ----------
    image : np.ndarray
        The image to plot.
    channels : list[int], optional
        Which channel to plot, by default [0] for a grayscale image.
    color : str, optional
        The color to plot the graph, by default 'k' for black.

    Returns
    -------
    plt.Figure:
        The MatPlotLib Image object on which was plotted.
    plt.Axes:
        The MatPlotLib Axes object on which was plotted.
    """
    hist = cv2.calcHist([image], channels, None, [256], [0, 256])
    fig, ax = plt.subplots()
    ax.plot(hist, color=color)
    ax.xlim([0, 256])
    ax.set_xlabel('Pixel value [uint8]')
    ax.set_ylabel('Counts')
    ax.show()
    return fig, ax