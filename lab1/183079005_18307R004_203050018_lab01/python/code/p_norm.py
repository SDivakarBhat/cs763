##Pratibha Varadkar (183079005)
## Lab 01- Python (P Norm)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("i_list", nargs="+", type = float, help='Array of integers')

parser.add_argument("--p", type=int)

args = parser.parse_args()

if args.p:
	pValue = args.p
else:
    pValue = 2

temp = [(abs(number))**pValue for number in args.i_list]
pNorm = (sum(temp))**(1/pValue)
print("Norm of ["+' '.join([str(elem) for elem in args.i_list]) +"] is "+ '%.2f'%pNorm )