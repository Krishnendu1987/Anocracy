#!/usr/bin/env python

import cv2
import numpy as np

#read image
img = cv2.imread(r"C:\Users\91990\Documents\Anocracy\FinalRoll\FinalRoll-page2.jpg")

original = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale

# threshold to get just the signature (INVERTED)
retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, \
                                   type=cv2.THRESH_BINARY_INV)

cnts , hierarchy = cv2.findContours(thresh_gray,cv2.RETR_LIST, \
                                       cv2.CHAIN_APPROX_SIMPLE)

#cnts = cnts[0] if len(cnts) == 2 else cnts[1]

ROI_number = 0
min_area = 50000
max_area = 250000

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = w*h
    
    if area > min_area and area < max_area:
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)
        ROI = original[y:y+h, x:x+w]
        img_name=f"C:/Users/91990/Documents/Anocracy/temp/Image_cont_{ROI_number}.jpg"
        cv2.imwrite(img_name.format(ROI_number), ROI)
        ROI_number += 1
