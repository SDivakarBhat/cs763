##Pratibha Varadkar (183079005)
## Lab 01- Numpy (Row Manipulation)

import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--N", type=int)
parser.add_argument('--oh',"--offset_height", type=int)
parser.add_argument('--ow',"--offset_width", type=int)
parser.add_argument('--th',"--target_height", type=int)
parser.add_argument('--tw',"--target_width", type=int)

args = parser.parse_args()
N = args.N
offset_height = args.oh
offset_width = args.ow
target_height = args.th
target_width = args.tw

#### 1.
a = list(range(N))
permArr = a[::2]+a[1::2]

E=np.identity(N)  #N X N identity matrix 
 
permutation=np.array([list(range(N)),permArr]) #the permutation in Cauchy 2 line form
 
P=np.zeros([N,N]) #initialize the permutation matrix
 
for i in range(N):
    P[i]=E[permutation[1][i]]

print("Original array:")
print(P)

#### 2.

def crop_array(arr_2d, offset_height, offset_width, target_height, target_width):
	return arr_2d[offset_height-1 : offset_height+target_height, offset_width-1 : offset_width+target_width]

croppedArr = crop_array(P, offset_height, offset_width, target_height, target_width)

print("Cropped Array:")
print(croppedArr)

#### 3. 

paddedArr = np.pad(croppedArr, ((2,2),(2,2)), 'constant', constant_values=0.5) 

print("Padded Array:")
print(paddedArr)

#### 4. 
concatArr = np.concatenate((paddedArr,paddedArr), axis = 1)

print("Concatenated Array: shape=" + str(concatArr.shape))
print(concatArr)