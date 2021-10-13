import os
import cv2
from pdf2image import convert_from_path

import pytesseract
import re
import numpy as np
from bnbphoneticparser import BengaliToBanglish
# import pandas library as pd
import pandas as pd

import json

try:
    from PIL import Image
except ImportError:
    import Image

path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram'
temp1_path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram\temp1'
temp2_path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram\temp2'

bengali2banglish = BengaliToBanglish()

df = pd.DataFrame(columns = ['Name', 'Age', 'Gender'])

#directory = r'C:\Users\91990\Documents\Anocracy\temp'
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def clean_age(age):
    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', age)]
    if not s:
        s = [0]
        s[0] = 0
    return s[0]

def clean_gender(gender):
    s = [str('পু') for s in re.findall(r'-?\d+\.?\d*', gender)]
    f = 'স্'
    m = 'পু'
    special_char = "N"
    regexpf = re.compile(f)
    regexpm = re.compile(m)
    if regexpf.search(gender):
        special_char = 'F'
    elif regexpm.search(gender):
        special_char = 'M'
    return special_char
oldfile = ''

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

list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(temp2_path, x)),os.listdir(temp2_path) ) )
latest_file = max(list_of_files)

for filename in os.listdir(temp2_path):
    fname = filename.split("-")[0] 
    latest_file_name = filename.split("-")[0]
    if fname != oldfile:
        
        
        # create an Empty DataFrame
        # object With column names only
        if oldfile != '':
            xslfname = oldfile + ".xlsx"
            xlsfpath = os.path.join(temp2_path, xslfname)
            df.to_excel(xlsfpath)
        df = pd.DataFrame(columns = ['Name', 'Age', 'Gender'])
        oldfile = fname
    else:
        if latest_file_name == fname:
            xslfname = oldfile + ".xlsx"
            xlsfpath = os.path.join(temp2_path, xslfname)
            df.to_excel(xlsfpath)
        
    
    f = os.path.join(temp2_path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print(f)
        f: str = f.replace('\\', '/')
        img = cv2.imread(f)
        #img1 = cv2.imread(f)
        #img = cv2.resize(img1,(350,200))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
        rho = 1
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 50  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        line_image = np.copy(img) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 1)
        # Draw the lines on the  image
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        # plt.imshow(lines_edges)
        # plt.show()
        text_from_image = pytesseract.image_to_string(lines_edges, lang="ben")
        #print(text_from_image)
        new_str = text_from_image.replace('\n', '')
        new_str = new_str.replace('স্বামীর নাম', '#')
        new_str = new_str.replace('পিতার নাম', '#')
        new_str = new_str.replace('গিতার নাম', '#')
        new_str = new_str.replace('নাম', '$')
        new_str = new_str.replace('বস', '@')
        new_str = new_str.replace('বয়স', '@')
        new_str = new_str.replace('ব্যস', '@')
        new_str = new_str.replace('লিঙ্গ', '&')
        #print('o/pval->', new_str)
        #new_str_name = []
        try:
            trgt_str:str = new_str.split('$')[1]
            new_str_name=trgt_str.split(':')[1].replace('#','')
            #translated_new_str_name = translator.translate(new_str_name,dest='en')
            translated_new_str_name = bengali2banglish.parse(new_str_name.strip()).upper()
            new_str_age=trgt_str.split(':')[4]
            new_str_gender=trgt_str.split(':')[5]
            clean_new_age = clean_age(new_str_age)
            clean_new_gender = clean_gender(new_str_gender)
            #print("Name :-> ",translated_new_str_name,"Age :-> ",new_str_age,"Gender :-> ",new_str_gender)
            #print("Name :-> ",translated_new_str_name,"Clean Age :-> ",clean_new_age,"Clean Gender :-> ",clean_new_gender)
            #str_clean_dict = 'hi'
            str_clean_dict = '{'+'"Name" : "'+str(translated_new_str_name)+'", "Age" : "'+str(clean_new_age)+'", "Gender" : "'+str(clean_new_gender)+'"'+'}'
            #print(str_clean_dict)
            Dict = json.loads(str_clean_dict)
            #print(Dict)
            df = df.append(Dict,ignore_index = True)
        except:
            #print(e)
            continue
