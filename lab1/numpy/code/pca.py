"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763-Lab1-numpy-pca
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt


def normalize_data(data):

    mu = data.mean(axis=0)
    sd = data.std(axis=0)
    data = data-mu/sd
    #data = data/np.max(data)
    return data


if __name__=='__main__':

    parse = argparse.ArgumentParser('pca')
    parse.add_argument('path',type=str, default='../data/housing.txt')

    args = parse.parse_args()

    array = np.loadtxt(args.path, dtype= float, delimiter=',').astype(float)
    #print(array.shape)
    data = normalize_data(array)

    eigenvecs, _ , _ = np.linalg.svd(data.T, full_matrices=False)
    projected = np.dot(data, (eigenvecs.T[:][:2]).T)
    #print(projected.shape, projected)
    plt.scatter(projected[:,0],projected[:,1],1)
    plt.title('CS763 Lab1 PCA')   
    plt.axes().set_aspect('equal')
    #plt.xlim(-15, 15)
    #plt.ylim(-15, 15)
    plt.savefig('../data/pca.png')
    plt.show()



