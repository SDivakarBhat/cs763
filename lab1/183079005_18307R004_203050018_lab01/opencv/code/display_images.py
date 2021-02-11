"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763_lab1_opencv_display_images
"""

import argparse
import cv2



if __name__=="__main__":

    parse = argparse.ArgumentParser('display_images')

    parse.add_argument('path', type=str, default='../data')

    args = parse.parse_args()
    idx = 0
    indices = ['00','01','02','03','04']
    cv2.namedWindow('Display carousel')
    image = cv2.imread(args.path+'/display{}.jpeg'.format(indices[idx]))
    while True:
        cv2.imshow("Display carousel", image)

        k = chr(cv2.waitKey(0))
        if k =='n':
            idx +=1
            image = cv2.imread(args.path+'/display{}.jpeg'.format(indices[idx%5]))
        elif k =='p':
            idx-=1
            image = cv2.imread(args.path+'/display{}.jpeg'.format(indices[idx%5]))

        elif k =='q':
            break
        else:
            print("Wrong key, Try Again")
