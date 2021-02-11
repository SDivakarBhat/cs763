"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763-Lab1-numpy-shape_manipulation
"""

import argparse
import numpy as np



if __name__=='__main__':

    parse = argparse.ArgumentParser('../data/shape_manipulation')

    parse.add_argument('path',type=str, default='grid_file.txt')
    
    args = parse.parse_args()

    M = int(input("M = "))
    N = int(input("N = "))
    
    array = np.loadtxt(args.path,delimiter=',').astype(np.float32)
    H,W = np.shape(array)
    print(np.repeat(array,(M*N)).reshape(M,N,H,W))


