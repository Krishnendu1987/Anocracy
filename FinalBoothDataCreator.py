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
temp1_path=r'C:\Users\91990\Documents\Anocracy\PurboMidnapore\NandiGram\temp2'
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
                    #page.save("%s-page%d.jpg" % (pdf_file, pages.index(page)), "JPEG")
                    #img = cv2.imread(page)
                    print(img_file)
                print(pdf_file)
                print(pages.index(page))
                
            #print(pdf_file)
