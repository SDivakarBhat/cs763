"""
Readme:
    Run the code and when the image appears, left click on the four corners to 
    select it. Following this use ESC key exit from the window. This will
    also then show the transformed image. Use ESC key to exit from thw display windows.
"""

import argparse
import cv2
from matplotlib import pyplot as plt
import numpy as np 

POINTS = []


def get_corners(event_name, x_coord, y_coord, flags, param):
    """
    get corner points from user based on the mouse left click
    arguments: event_name, x_coord, y_coord, flags, param
    """
    global POINTS
    if event_name == cv2.EVENT_LBUTTONDOWN:
        POINTS.append((x_coord, y_coord))
    #POINTS = np.array(POINTS)
    if len(POINTS) > 4:
        return
    pass


def get_dist(A, B):
    """
    calculate distance based on input coordintes

    arguments: two points A and B
    returns: distance
    """
    return np.sqrt(((A[0]-B[0])**2) + ((A[1]-B[1])**2))



if __name__ == "__main__":
    PARSE = argparse.ArgumentParser('document-scanner')
    PARSE.add_argument('-i', type=str, default='../data/scan.jpg')
    ARGS = PARSE.parse_args()
    IMAGE = cv2.imread(ARGS.i)
    cv2.namedWindow('Image_Original', cv2.WINDOW_NORMAL)
    cv2.imshow('Image_Original', IMAGE)
    cv2.setMouseCallback('Image_Original', get_corners)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    POLY = []
    # POINTS = get_corners()
    CORNERS = POINTS.copy()
    POINTS = np.array(POINTS)
    ADD = POINTS.sum(axis=1)
    POLY.append(POINTS[np.argmin(ADD)])
    POLY.append(POINTS[np.argmax(ADD)])

    SUB = np.diff(POINTS, axis=1)
    POLY.append(POINTS[np.argmin(SUB)])
    POLY.append(POINTS[np.argmax(SUB)])
    print('POLY', POLY)
    TEMP = IMAGE.copy()
    cv2.polylines(TEMP, [np.array(POLY)], True, (0, 255, 0), 7)
    cv2.imshow('Image_Original', TEMP)

    (TOP_LEFT, TOP_RIGHT, BOTTOM_RIGHT, BOTTOM_LEFT) = POLY
    
    # possible to calculate the target width and height
    # But in this asssignment we are keeping it fixed to 400 and 600

    NEW_W_A = get_dist(BOTTOM_RIGHT, BOTTOM_LEFT)
    NEW_W_B = get_dist(TOP_RIGHT, TOP_LEFT)
    MAX_WIDTH = 400 #max(int(NEW_W_A), int(NEW_W_B))

    NEW_H_A = get_dist(TOP_RIGHT, BOTTOM_RIGHT)
    NEW_H_B = get_dist(TOP_LEFT, BOTTOM_LEFT)
    MAX_HEIGHT = 600 #max(int(NEW_H_A), int(NEW_H_B))
    NEW_DIM = np.array([[0, 0], [400, 0], [400, 600], [0, 600]], dtype="float32")# np.array([[0, 0], [MAX_WIDTH-1, 0], [MAX_WIDTH-1,                                                                                  #  MAX_HEIGHT-1], [0, MAX_HEIGHT-1]], dtype="float32                                                                                 #")
    MAT = np.array(CORNERS, dtype="float32")
    MATRIX = cv2.getPerspectiveTransform(MAT, NEW_DIM)
    SCANNED = cv2.warpPerspective(IMAGE, MATRIX, (MAX_WIDTH, MAX_HEIGHT))
    cv2.namedWindow('Transformed', cv2.WINDOW_NORMAL)                                                                                    #cv2.polylines(IMAGE, [np.array(POLY)], True, (0, 255, 0), 7)
    #cv2.imshow('Input image', IMAGE)
    cv2.imshow("Image_Original", IMAGE)
    cv2.imshow("Transformed", SCANNED)
    cv2.waitKey(0)
    cv2.imwrite("../data/transformed-image.jpg", SCANNED)
