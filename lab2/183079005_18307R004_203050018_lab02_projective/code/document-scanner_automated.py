import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i")
args = parser.parse_args()

distorted_img = cv2.imread(args.i)
distorted_img_copy = cv2.imread(args.i)
xmax,ymax = 1500,2000

# automatic points detection
distorted_img_gray = cv2.cvtColor(distorted_img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(distorted_img_gray,127,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# identifying contour with max area
max_area = 0
max_cnt = []
for cnt in contours:
	area = cv2.contourArea(cnt)
	if max_area < area:
		max_area = area
		max_cnt.append(cnt)

cnt = max_cnt[-1]
# draw contour with max area
distorted_img_with_contour = cv2.drawContours(distorted_img,cnt,-1,(0,255,0),3)

# fit polygon on contour
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)
x_sorted_pts = approx[approx.argsort(axis=0)][:,0,0]
# draw polygon fit on image
cv2.drawContours(distorted_img_with_contour, [approx], 0, (255,255,255), 3)
if approx.shape[0] == 4:
	# ordering points
	# left points
	xmin_1 = x_sorted_pts[0][0]
	xmin_2 = x_sorted_pts[1][0]
	if xmin_1[1] < xmin_2[1]:
		p1 = xmin_1
		p2 = xmin_2
	else:
		p1 = xmin_2
		p2 = xmin_1
	# right points
	xmin_3 = x_sorted_pts[2][0]
	xmin_4 = x_sorted_pts[3][0]
	if xmin_3[1] < xmin_4[1]:
		p3 = xmin_3
		p4 = xmin_4
	else:
		p3 = xmin_4
		p4 = xmin_3

	# marking identified points
	cv2.circle(distorted_img_with_contour, tuple(p1), 20, (0,0,255), -1)
	cv2.circle(distorted_img_with_contour, tuple(p2), 20, (0,0,255), -1)
	cv2.circle(distorted_img_with_contour, tuple(p3), 20, (0,0,255), -1)
	cv2.circle(distorted_img_with_contour, tuple(p4), 20, (0,0,255), -1)
	detected_pts = np.float32([list(p1),list(p2),list(p3),list(p4)])
	quad_pts = np.float32([[0,0],[0, ymax],[xmax, 0],[xmax,ymax]])

	M = cv2.getPerspectiveTransform(detected_pts,quad_pts)
	automated_undistored_img = cv2.warpPerspective(distorted_img_copy,M,(xmax,ymax))

else:
	print("Unable to identify correct points")

cv2.namedWindow("Binary Image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Binary Image", 600,600)
cv2.imshow("Binary Image",thresh)
cv2.namedWindow("Distorted Image With Contour",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Distorted Image With Contour", 600,600)
cv2.imshow("Distorted Image With Contour",distorted_img_with_contour)
if approx.shape[0] == 4:
	cv2.namedWindow("Automated Undistored Image",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Automated Undistored Image", 600,600)
	cv2.imshow("Automated Undistored Image",automated_undistored_img)
	storedimg2 = cv2.imwrite("../results/document-scanner.png",automated_undistored_img)
cv2.waitKey(0)
cv2.destroyAllWindows()



# https://stackoverflow.com/questions/41138000/fit-quadrilateral-tetragon-to-a-blob
