"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763-Lab1-Python
"""

import argparse


if __name__=='__main__':


    parse = argparse.ArgumentParser('p_norm')

    parse.add_argument('num', nargs="+", type=float)
    parse.add_argument('--p', type=int,default=2)

    args = parse.parse_args()

    result = 0
    for x in args.num:
        result += abs(x)**args.p
    result = result**(1/args.p)
    print("Norm of {0} is {1:.2f}".format(args.num,result))
