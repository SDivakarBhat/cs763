"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763_lab1_opencv_image_conversion
"""


import numpy as np
import cv2 
import matplotlib.pyplot as plt
import argparse





if __name__=='__main__':

    parse =  argparse.ArgumentParser('image_conversion')

    parse.add_argument('path',type=str, default='../data/test.jpeg')

    args = parse.parse_args()


    image1 = cv2.imread(args.path)
    
    image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    array = np.asarray(image)
    norm_image = np.zeros_like(image)
    norm_image = cv2.normalize(image,norm_image,alpha=0,beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)


    fig, axs = plt.subplots(1,2)
    axs[0].imshow(image)
    axs[0].title.set_text("Original image")
    axs[1].imshow(norm_image)
    axs[1].title.set_text("Normalized image")
    plt.suptitle("Figure1: Plotting images using matplotlib",y=0.1)
    plt.savefig('../data/image_conversion_matplotlib.png')
    plt.show()

    #cv2.namedWindow("Original image")
    #cv2.namedWindow("Normalized image")
    #cv2.resizeWindow("Original image",600,600)
    #cv2.resizeWindow("Normalized image",600,600)
    cv2.imshow("Original image",image1)
    cv2.imshow("Normalized image", norm_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('../data/test_opencv_original.jpeg',image1)
    cv2.imwrite('../data/test_opencv_normalized.jpeg',norm_image)



