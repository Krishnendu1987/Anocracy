import os
import cv2
from pdf2image import convert_from_path

import numpy as np
from bnbphoneticparser import BengaliToBanglish
try:
    from PIL import Image
except ImportError:
    import Image

path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram'
temp1_path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram\temp1'
temp2_path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram\temp2'
for filename in os.listdir(path):
    pdf_file = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(pdf_file):
        # print(f)
        pdf_file: str = pdf_file.replace('\\', '/')
        # checking if it is a pdf file or not
        if pdf_file.endswith(".pdf"):
            pages = convert_from_path(pdf_file, 300,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
            #temp_img_file = os.path.join(temp1_path, filename)
            #temp_img_file = temp_img_file[:-4]
            #temp_img_file: str = temp_img_file.replace('\\', '/')
            pdf_file = pdf_file[:-4]
            img_file_name = pdf_file.split('/')[-1]
            img_file = os.path.join(temp1_path, img_file_name)
            img_file: str = img_file.replace('\\', '/')
            for page in pages:
                if pages.index(page) > 1 and pages.index(page) is not len(pages)-1 :
                    page.save("%s-page%d.jpg" % (img_file, pages.index(page)), "JPEG")
                    #img = cv2.imread(page)
                    print(img_file)
                print(pdf_file)
                print(pages.index(page))
                
            #print(pdf_file)
for filename1 in os.listdir(temp1_path):
    img_file1 = os.path.join(temp1_path, filename1)
    if os.path.isfile(img_file1):
        img_file1: str = img_file1.replace('\\', '/')
        #mg_file_name1 = img_file1.split('/')[-1]
        img_file_name1 = img_file1.split('/')[-1]
        img = cv2.imread(img_file1)
        original = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
        # threshold to get just the signature (INVERTED)
        retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, \
                                   type=cv2.THRESH_BINARY_INV)
        cnts , hierarchy = cv2.findContours(thresh_gray,cv2.RETR_LIST, \
                                       cv2.CHAIN_APPROX_SIMPLE)
        img_file_name1 = img_file_name1[:-4]
        ROI_number = 0
        min_area = 50000
        max_area = 250000
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            area = w*h
            if area > min_area and area < max_area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)
                ROI = original[y:y+h, x:x+w]
                
                #mg_file_name2 =str(img_name1) +"_img_cnt_" + {ROI_number} +".jpg"
                img_file_name2 = str(img_file_name1) + "_img_cnt_" + str(ROI_number) +".jpg"
                img_file2= os.path.join(temp2_path, img_file_name2)
                img_file2: str = img_file2.replace('\\', '/')
                #mg_name=f"C:/Users/91990/Documents/Anocracy/temp/Image_cont_{ROI_number}.jpg"
                cv2.imwrite(img_file2.format(ROI_number), ROI)
                ROI_number += 1
