"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763_lab2_affine_transformation
Date: 3rd February 2021
"""


import argparse
import cv2



if __name__ =="__main__":

    parse = argparse.ArgumentParser('Affine Transformation')

    parse.add_argument('-mat', type=str, default='manual')
    parse.add_argument('--path', type=str, default='../data/distorted.jpg')
    args = parse.parse_args()


    


    
