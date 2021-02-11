##Pratibha Varadkar (183079005)
## Lab 01- Numpy (Shape Manipulation)

import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("filepath")

args = parser.parse_args()
fpath = args.filepath

with open(fpath) as textFile:
    mat = [line.rstrip().split(',') for line in textFile]

mat = np.array([list( map(int,i) ) for i in mat])

M = int(input("Enter your value of M: "))
N = int(input("Enter your value of N: "))

out = []	
for i in range(mat.shape[0]):
	temp = []
	for j in range(mat.shape[1]):
		temp.append([[mat[i,j] for y in range(N)] for z in range(M)] )
	out.append(temp)

print(out)