"""
Written by S Divakar Bhat
Roll No: 18307R004
Title: Auto Mosaicing
"""
import argparse
import cv2
import numpy as np
# import os

POINTS = []


def get_kps_ftrs(image):
    """
    Function to get keypoints and featured of image 
    using ORB
    """
    orb = cv2.ORB_create()
    return orb.detectAndCompute(image, None)


def find_homography(corr):
    """
    Function to find the homography matrix based on the given input
    correspondence points
    """
    global POINTS
    # homo = []
    pts_src = np.array(POINTS[1::2])
    pts_dst = np.array(POINTS[::2])
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
    # TEMP1 = IMAGE1.copy()
    # TEMP2 = IMAGE2.copy()
    KPS1, FTRS1 = get_kps_ftrs(IMAGE1)
    KPS2, FTRS2 = get_kps_ftrs(IMAGE2)
    MATCHER = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    MATCHED = MATCHER.match(FTRS1, FTRS2)
    KPS1 = np.array([kps.pt for kps in KPS1])
    KPS2 = np.array([kps.pt for kps in KPS2])
    PTS1 = np.array([KPS1[x.queryIdx] for x in MATCHED])
    PTS2 = np.array([KPS2[x.trainIdx] for x in MATCHED])
    H, _ = cv2.findHomography(PTS1, PTS2, cv2.RANSAC, 5)
    # print(len(H))
    IMAGE_1 = cv2.warpPerspective(IMAGE1, H, (IMAGE1.shape[1]
                                              + IMAGE2.shape[1],
                                              IMAGE1.shape[0]+IMAGE2.shape[0]))
    H_1, W_1 = IMAGE1.shape[:2]
    H_2, W_2 = IMAGE2.shape[:2]
    # RESULT = np.zeros((max(H_1, H_2), W_1+W_2, 3), dtype="uint8")
    IMAGE_1[0:H_2, 0:W_2] = IMAGE2
    # RESULT[0:H_2, W_2:] = IMAGE_1[0:H_1, 0:W_1]
    cv2.imshow("Image 1", IMAGE1)
    cv2.imshow("Image 2", IMAGE2)
    cv2.imshow("Result", IMAGE_1)

    cv2.waitKey(0)
