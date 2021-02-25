"""
Written by S Divakar Bhat
Roll No: 18307R004
Title: Manual Mosaicing
"""
import argparse
import cv2
import numpy as np
# import os

POINTS = []

def get_point(event_name, x_coord, y_coord, flags, param):
    """
    get the points clicked by user
    """
    global POINTS
    if event_name == cv2.EVENT_LBUTTONDOWN:
        POINTS.append((x_coord, y_coord))


def get_correspondence(image1, image2):
    """
    Function to get correspondence points from user
    """
    corr = []
    cv2.namedWindow('Image 1', cv2.WINDOW_NORMAL)
    cv2.imshow('Image 1', image1)
    cv2.namedWindow('Image 2', cv2.WINDOW_NORMAL)
    cv2.imshow('Image 2', image2)
    while True:
        c = cv2.waitKey(7) % 0x100
        if c == 27: # or c == 10:
            break
        else:
            cv2.setMouseCallback('Image 1', get_point)
            cv2.setMouseCallback('Image 2', get_point)
    corr = POINTS.copy()
    pts2 = POINTS[1::2]
    pts1 = POINTS[::2]
    for pts in pts1:
        cv2.circle(image1, pts, 5, (0, 0, 255), -1)
    for pts in pts2:
        cv2.circle(image2, pts, 5, (0, 0, 255), -1)

    return corr


def find_homography(corr):
    """
    Function to find the homography matrix based on the given input
    correspondence points
    """
    global POINTS
    # homo = []
    pts_dst = np.array(POINTS[1::2])
    pts_src = np.array(POINTS[::2])
    homo, _ = cv2.findHomography(pts_src, pts_dst, cv2.RANSAC, 5.0)
    return homo


if __name__ == "__main__":
    PARSE = argparse.ArgumentParser('manual mosaicing')
    PARSE.add_argument('path', type=str, default='../data/manual/campus/')
    ARGS = PARSE.parse_args()
    IMAGE1_PATH = ARGS.path + 'campus{}.jpg'.format(1)
    IMAGE2_PATH = ARGS.path + 'campus{}.jpg'.format(2)
    IMAGE1 = cv2.imread(IMAGE1_PATH)
    IMAGE2 = cv2.imread(IMAGE2_PATH)
    TEMP1 = IMAGE1.copy()
    TEMP2 = IMAGE2.copy()
    CORR = get_correspondence(TEMP1, TEMP2)
    H = find_homography(CORR)
    IMAGE_1 = cv2.warpPerspective(IMAGE1, H, (IMAGE1.shape[1]
                                             + IMAGE2.shape[1],
                                             IMAGE1.shape[0]+IMAGE2.shape[0]))
    H_1, W_1 = IMAGE1.shape[:2]
    H_2, W_2 = IMAGE2.shape[:2]
    # RESULT = np.zeros((max(H_1, H_2), W_1+W_2, 3), dtype="uint8")
    IMAGE_1[0:H_2, 0:W_2] = IMAGE2
    # RESULT[0:H_2, W_2:] = IMAGE_1[0:H_1, 0:W_1]
    cv2.imshow("Image 1", TEMP1)
    cv2.imshow("Image 2", TEMP2)
    cv2.imshow("Result", IMAGE_1)

    cv2.waitKey(0)
