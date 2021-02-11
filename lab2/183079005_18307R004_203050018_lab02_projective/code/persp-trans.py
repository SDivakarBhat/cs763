import cv2
import numpy as np 

i = 0
img = cv2.imread('../data/obelisk.png')
height, width, _ = img.shape 

## Used to find the coordinates of the 4 corners

# cv2.circle(img, (217,240), 5, (0,0,255), -1)
# cv2.circle(img, (478,183), 5, (0,0,255), -1)
# cv2.circle(img, (703,1028), 5, (0,0,255), -1)
# cv2.circle(img, (990,828), 5, (0,0,255), -1)

## Save the transformed image of map
p1 = np.float32([[478,183], [990,828], [217,240], [703,1028]])
p2 = np.float32([[0,0], [512,0], [0,385], [512,385]])
matrix = cv2.getPerspectiveTransform(p1, p2)
final = cv2.warpPerspective(img, matrix, (512,385))
cv2.imwrite("../results/obeliskTransformed.png", final)

while True:

	P1_1 = np.linspace(478,0)
	P1_2 = np.linspace(183,0)

	P2_1 = np.linspace(990,512)
	P2_2 = np.linspace(828,0)

	P3_1 = np.linspace(217,0)
	P3_2 = np.linspace(240,385)

	P4_1 = np.linspace(703,512)
	P4_2 = np.linspace(1028,385)

	itv = 50

	pts1 = np.float32([[478,183], [990,828], [217,240], [703,1028]])
	pts2 = np.float32([[P1_1[i],P1_2[i]], [P2_1[i],P2_2[i]], [P3_1[i],P3_2[i]], [P4_1[i],P4_2[i]]])

	matrix = cv2.getPerspectiveTransform(pts1, pts2)

	final = cv2.warpPerspective(img, matrix, (height,width))

	pts = np.array([[P1_1[i],P1_2[i]], [P2_1[i],P2_2[i]], [P4_1[i],P4_2[i]], [P3_1[i],P3_2[i]]])

	## (1) Crop the bounding rect
	rect = cv2.boundingRect(pts.astype(np.int))
	x,y,w,h = rect
	croped = final[y:y+h, x:x+w].copy()

	## (2) make mask
	pts = pts - pts.min(axis=0)
	mask = np.zeros(croped.shape[:2], np.uint8)
	cv2.drawContours(mask, [pts.astype(np.int)], -1, (255, 255, 255), -1, cv2.LINE_AA)

	## (3) do bit-op
	dst = cv2.bitwise_and(croped, croped, mask=mask)

	## (4) add the white background
	bg = np.ones_like(croped, np.uint8)*255
	cv2.bitwise_not(bg,bg, mask=mask)
	dst2 = bg + dst

	i = (i+1)%itv

	cv2.imshow("Final",dst2)

	if cv2.waitKey(50) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()