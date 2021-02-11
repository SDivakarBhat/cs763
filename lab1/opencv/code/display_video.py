"""
Written by: S Divakar Bhat
Roll No: 18307R004
Title: CS763_lab1_opencv_display_images
"""

import argparse
import cv2



if __name__=="__main__":

    parse = argparse.ArgumentParser('display_video')

    parse.add_argument('path', type=str, default='../data/sample_video.mp4')

    args = parse.parse_args()

    vid = cv2.VideoCapture(args.path)
    
    while True:

        _, frame = vid.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.rectangle(frame, (400,22), (636,1), (255,0,0), (1))
        cv2.putText(frame,'S Divakar Bhat', (400,23),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)        
        cv2.rectangle(gray, (400,22), (636,1), (255,0,0), (1))
        cv2.putText(gray,'S Divakar Bhat', (400,23),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)
        cv2.imshow('Original',frame)
        cv2.imshow('Grayscale',gray)
        cv2.moveWindow('Grayscale',680,55)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #vid.release()
    cv2.destroyAllWindows()
    vid.release()
