"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: cs763_lab2_document-scanner
"""

import argparse
import cv2
from matplotlib import pyplot as plt

if __name__ == "__main__":
    PARSE = argparse.ArgumentParser('document-scanner')
    PARSE.add_argument('-i', type=str, default='../data/scan.jpg')
    ARGS = PARSE.parse_args()
    IMAGE = cv2.imread(ARGS.i)
    GRAY = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)
    GRAY = cv2.GaussianBlur(GRAY, (7, 7), 0)
    EDGE_IMAGE = cv2.Canny(GRAY, 100, 150)
    plt.subplot(121)
    plt.imshow(GRAY, cmap='gray')
    plt.subplot(122)
    plt.imshow(EDGE_IMAGE, cmap='gray')
    plt.show()
    
    

    """
    CONTOUR, _ = cv2.findContours(EDGE_IMAGE.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #   print(CONTOUR)
    #   CNT = CONTOUR[0]
    #   print(cv2.contourArea(CONTOUR))
    #CONTOUR = sorted(CONTOUR, key=cv2.contourArea, reverse=True)[:5]
    CONTOUR = max(CONTOUR, key=cv2.contourArea)
    CONTOUR_IMAGE = cv2.drawContours(IMAGE.copy(), CONTOUR, -1, (0, 255, 0), 3)
    plt.imshow(CONTOUR_IMAGE)
    plt.show()
    #   LEFT = tuple(CONTOUR[CONTOUR[:, :, 0].argmin()][0])
    #   RIGHT = tuple(CONTOUR[CONTOUR[:, :, 0].argmax()][0])
    #   TOP = tuple(CONTOUR[CONTOUR[:, :, 1].argmin()][0])
    #   BOTTOM = tuple(CONTOUR[CONTOUR[:, :, 1].argmax()][0])
    AREA = 0
    for cnt in CONTOUR:
        epsilon = 0.02*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if(len(approx) == 4):
            DOC_CONTOUR = approx
            break
    print(DOC_CONTOUR)
    BOUND_POINT = cv2.drawContours(IMAGE.copy(), DOC_CONTOUR, -1, (0, 255, 0), 3)
    plt.imshow(BOUND_POINT)
    plt.show()

    #print(CONTOUR)
    """
