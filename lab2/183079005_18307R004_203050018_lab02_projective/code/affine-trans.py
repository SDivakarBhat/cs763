import cv2
import argparse
import numpy as np

# parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-mat",choices=['manual','api'])
args = parser.parse_args()

# reading distorted image
given_img = cv2.imread('../data/distorted.jpg')
xmax,ymax = 600,600

# computing tranformation matrix
if(args.mat=='manual'):
	shear_mat = np.float32([[1,-0.1,0],[-0.1,1,0]])
	M = shear_mat
if(args.mat=='api'):
	# points in given Image    B        A         C
	given_pts = np.float32([[60,600],[600,60],[660,660]])
	# points in original image
	trans_pts = np.float32([[0,ymax],[xmax,0],[xmax,ymax]])
	M = cv2.getAffineTransform(given_pts,trans_pts)

# getting transformed image
trans_img = cv2.warpAffine(given_img,M,(xmax,ymax))

cv2.imshow('Distorted Image',given_img)
cv2.namedWindow("Transformed Image")
cv2.moveWindow("Transformed Image",1000,200)
cv2.imshow('Transformed Image',trans_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
