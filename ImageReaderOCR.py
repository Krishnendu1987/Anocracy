#!/usr/bin/env python
# coding: utf-8

from PIL import Image
from pytesseract import pytesseract
#https://github.com/nikhilkumarsingh/tesseract-python
#https://github.com/cseas/ocr-table
# Defining paths to tesseract.exe
# and the image we would be using
#C:\Program Files\Tesseract-OCR
#C:\Users\91990\Downloads\223_Form20-compressed\223_Form20-compressed-01.jpeg
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Users\91990\Documents\Anocracy\FinalRoll\FinalRoll-page2.jpg"

# Opening the image & storing it in an image object
img = Image.open(image_path)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img,lang="ben")

new_str=text.replace('\n','')
new_str=new_str.replace('স্বামীর নাম','#')
new_str=new_str.replace('পিতার নাম','#')
new_str=new_str.replace('নাম','$')
new_str=new_str.replace('বস','@')
new_str=new_str.replace('বয়স','@')
new_str=new_str.replace('ব্যস','@')
new_str=new_str.replace('লিঙ্গ','&')



new_str_name=[]

for xx in new_str.split('$'):
    print('Line1 ',xx)

    new_str_name.append(xx.split(':')[0])
    print('Line2 ',xx.split(':'))


print(len(new_str_name))
title : list =[]
for x in range(len(new_str_name)):
    new_str_name_list=new_str_name[x].split(' ')

    if new_str_name_list[len(new_str_name_list)-1] == '':
        try:
            title.append(new_str_name_list[len(new_str_name_list)-2] )
        except:
            pass
    else:
        title.append(new_str_name_list[len(new_str_name_list)-1])

print(title)
#print(new_str_name[3])
#print(new_str_name[15])
# Displaying the extracted text
#print(new_str_name)