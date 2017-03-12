import cv2
import numpy as np


def smooth1(img):
    ret1, th1 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(img, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imwrite('metaa.tiff' , th3)
    return th3


def smooth2(file_name):
    img = cv2.imread(file_name, 0)
    # smooth1(img)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = smooth1(img)  # cv2.imread('metaa.tiff' , 0)
    closing = cv2.bitwise_or(img, closing)
    return closing

# smooth2('1.jpg')
