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
    Input: two images
    Output: Homography matrix
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
    homo, _ = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5)
    return homo


def assign_pxl(img1, img2):
    """
    assign pixel values by comparing the pixel locatiosn of left
    and warped image on right
    Input: Left and right image
    Output: combined image
    """
    h_1, w_1 = img1.shape[:2]
    for i in range(w_1):
        for j in range(h_1):
            if(np.array_equal(img1[j, i], np.array([0, 0, 0])) and
               (np.array_equal((img2[j, i]), np.array([0, 0, 0])))):
                img2[j, i] = [0, 0, 0]
            elif np.array_equal(img2[j, i], np.array([0, 0, 0])):
                img2[j, i] = img1[j, i]
    return img2


def generalised_mosaic(images, ref_id):
    """
    function for generalised panormaic mosaicing from given n images
    Input: set of images and reference image id
    Output: Stitched image
    """

    left = images[0:ref_id]
    right = images[ref_id:]
    # print(len(left), len(right), len(images))

    left_1 = left[0]
    for img in left[1:]:
        inv_h = get_homography(img, left_1)
        f_1 = np.dot(inv_h, np.array([0, 0, 1]))
        inv_h[0][-1] += abs(f_1[0])
        inv_h[1][-1] += abs(f_1[1])
        y_shift = abs(int(f_1[1]))
        x_shift = abs(int(f_1[0]))
        dest_size = (left_1.shape[1]+img.shape[1],
                     left_1.shape[0]+img.shape[0])
        temp = cv2.warpPerspective(left_1, inv_h, dest_size)
        temp[y_shift:img.shape[0]+y_shift, x_shift:img.shape[1]+x_shift] = img
        left_1 = temp
    # return temp

    for img in right:
        homo = get_homography(left_1, img)
        dest_dim = np.dot(homo, np.array([img.shape[1],
                                          img.shape[0], 1]))
        dest_dim = dest_dim/dest_dim[-1]
        dest_size = (left_1.shape[1]+img.shape[1],
                     left_1.shape[0]+img.shape[0])
        temp = cv2.warpPerspective(img, homo, dest_size)
        temp = assign_pxl(left_1, temp)
        left_1 = temp
    result = temp
    return result


if __name__ == "__main__":
    PARSE = argparse.ArgumentParser('Generalised Mosaicing')
    PARSE.add_argument('dir', type=str, default='../data/general/mountain/')
    PARSE.add_argument('ref_idx', type=int)
    ARGS = PARSE.parse_args()
    IMAGES = []
    for _, _, file_ in os.walk(ARGS.dir):
        file_.sort()
        for f in file_:
            image_path = ARGS.dir+'{}'.format(f)
            # print(image_path)
            IMAGES.append(cv2.imread(image_path))
    # print(len(IMAGES))
    print('---Generating Panorama. Please wait !!!---')
    OUTPUT = generalised_mosaic(IMAGES, ARGS.ref_idx)

    # Crop the image to remove as much black border as possible
    GRAY = cv2.cvtColor(OUTPUT, cv2.COLOR_BGR2GRAY)
    _, THRESH = cv2.threshold(GRAY, 1, 255, cv2.THRESH_BINARY)
    CONTOURS, _ = cv2.findContours(THRESH, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    CNT = CONTOURS[0]
    X, Y, W, H = cv2.boundingRect(CNT)
    CROP = OUTPUT[Y:Y+H, X:X+W]
    # print(ARGS.dir.split('/'))
    WRITE_PATH = '../results/pano-general-results/{}'\
                 .format(ARGS.dir.split('/')[-2])+'.png'
    # print(WRITE_PATH)
    cv2.imwrite(WRITE_PATH, CROP)
    cv2.namedWindow('RESULT', cv2.WINDOW_NORMAL)
    cv2.imshow('RESULT', CROP)
    cv2.waitKey(0)
