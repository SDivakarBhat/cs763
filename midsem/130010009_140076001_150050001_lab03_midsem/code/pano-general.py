"""
Written by S Divakar Bhat
Roll No: 18307R004
Title: Generalised panoramic mosaicing
"""

import argparse
import os
import cv2
import numpy as np
# import matplotlib.pyplot as plt

def get_kps_ftrs(image):
    """
    Function to get keypoints and features of image using ORB
    """
    orb = cv2.ORB_create()
    return orb.detectAndCompute(image, None)


def get_homography(ref_image, image2):
    """
    Get homography matrix for each pair of images
    """
    kps1, ftrs1 = get_kps_ftrs(ref_image)
    kps2, ftrs2 = get_kps_ftrs(image2)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matched = matcher.match(ftrs1, ftrs2)
    matched.sort(key=lambda x: x.distance)
    matched = matched[:int(len(matched)*0.9)]
    kps1 = np.array([kps.pt for kps in kps1])
    kps2 = np.array([kps.pt for kps in kps2])
    pts1 = np.array([kps1[x.queryIdx] for x in matched])
    pts2 = np.array([kps2[x.trainIdx] for x in matched])
    homo, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, 4)
    return homo


def generalised_mosaic(images, ref_id):
    """
    function for generalised panormaic mosaicing from given n images
    """
    # print(images)
    ref_img = images[ref_id-1]
    # images.pop(ref_id-1)
    h_out = 0
    w_out = 0
    homo = []
    tot_hom = []
    for img in images:
        h_out += img.shape[0]
        w_out += img.shape[1]
    for _, img in enumerate(images):
        homo.append(get_homography(ref_img, img))
    for hom in homo:
        
    prev = None
    image_homo_pair = zip(images, homo)
    for img, h_ in image_homo_pair:

        result = cv2.warpPerspective(img, h_, (h_out, w_out))
        if not prev:
            r
            cv2.namedWindow('RESULT', cv2.WINDOW_NORMAL)
            cv2.imshow('RESULT', result)
            cv2.waitKey(0)
        prev = img
    return result


if __name__ == "__main__":
    PARSE = argparse.ArgumentParser('Generalised Mosaicing')
    PARSE.add_argument('dir', type=str, default='../data/general/mountain/')
    PARSE.add_argument('ref_idx', type=int)
    ARGS = PARSE.parse_args()
    IMAGES = [] # set()
    for _, _, file_ in os.walk(ARGS.dir):
        file_.sort()
        for f in file_:
            image_path = ARGS.dir+'{}'.format(f)
            print(image_path)
            IMAGES.append(cv2.imread(image_path))
    print(len(IMAGES))
    OUTPUT = generalised_mosaic(IMAGES, ARGS.ref_idx)
    cv2.namedWindow('RESULT', cv2.WINDOW_NORMAL)
    cv2.imshow('RESULT', OUTPUT)
    cv2.waitKey(0)
