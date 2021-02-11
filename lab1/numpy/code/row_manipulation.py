"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763-Lab1-numpy-row_manipulation
"""

import argparse
import numpy as np

def permute_matrix(N):

    eye = np.identity(N)
    P = np.zeros((N,N))
    if N%2==0:
        idx = N//2
    else:
        idx = N//2+1

    P[0::2] = eye[:idx]
    P[1::2] = eye[idx:]
    return P

def crop_array(arr_2d, offset_height, offset_width, target_height, target_width):

    cropped_array = arr_2d[offset_height:offset_height+target_height,offset_width:offset_width+target_width]

    return cropped_array

def pad_array(arr_2d, padder, pad_width):
    m,n = np.shape(arr_2d)
    padded_array = np.full((m+(2*pad_width),n+(2*pad_width)),padder)
    padded_array[pad_width:m+pad_width,pad_width:n+pad_width]=arr_2d
    return padded_array

def concat_array(arr_2d):

    return np.hstack((arr_2d,arr_2d))

if __name__=='__main__':

    parse = argparse.ArgumentParser('row_manipulation')
    parse.add_argument('--N', type=int)
    

    args = parse.parse_args()

    P = permute_matrix(args.N)
    print("Original array:\n",P)
    cropped_array = crop_array(P,1,1,2,2)
    print("\nCropped array:\n",cropped_array)
    padded_array = pad_array(cropped_array,0.5,2)
    print("\nPadded array:\n",padded_array)
    concatenated_array = concat_array(padded_array)
    print("\nConcatenated array: shape={}\n{}".format(np.shape(concatenated_array),concatenated_array))
