import cv2
import numpy as np

def line_img(img):
    neiborhood8 = np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]], np.uint8)

    img_dilate = cv2.dilate(img, neiborhood8, iterations=2)
    img_diff = cv2.absdiff(img, img_dilate)
    img_diff_not = cv2.bitwise_not(img_diff)
    gray = cv2.cvtColor(img_diff_not, cv2.COLOR_BGR2GRAY)

    return gray
