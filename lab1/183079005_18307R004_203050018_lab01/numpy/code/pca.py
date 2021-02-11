##Pratibha Varadkar (183079005)
## Lab 01- Numpy (PCA)

import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("filepath")

args = parser.parse_args()
fpath = args.filepath

with open(fpath) as textFile:
    data = [line.rstrip().split(',') for line in textFile]

data = np.array([list( map(float,i) ) for i in data])

data = data - data.mean(axis=0)
covMat = np.cov(data.T) / data.shape[0]
eigVal, eigVec = np.linalg.eig(covMat)
idx = eigVal.argsort()[::-1]
eigVal = eigVal[idx]
eigVec = eigVec[:,idx]

redDimData = data.dot(eigVec[:, :2]) #since number of dimensions required is two.

plt.scatter(redDimData[:,0], redDimData[:,1])
plt.xlabel('Dim 0')
plt.ylabel('Dim 1')
plt.xlim(-15,15)
plt.ylim(-15,15)
plt.savefig('out.png')
plt.show()
