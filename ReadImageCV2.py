import pytesseract
import matplotlib.pyplot as plt
import cv2
from PLI import image

image_path = r"C:\Users\91990\Documents\Anocracy\FinalRoll\FinalRoll-page2.jpg"
im = cv2.imread(image_path)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
dilate = cv2.dilate(thresh, kernel, iterations=4)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
line_items_coordinates = []
for c in cnts:
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c)
    if y >= 600 and x <= 1000:
        if area > 10000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])
            
    if y >= 2400 and x<= 2000:
        image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
        line_items_coordinates.append([(x,y), (2200, y+h)])
    
    else:
        image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
        line_items_coordinates.append([(x,y), (2200, y+h)])
        
    
        
        
print(line_items_coordinates)


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Users\91990\Documents\Anocracy\FinalRoll\FinalRoll-page2.jpg"
image = cv2.imread(image_path)

for c in line_items_coordinates:
    print(c)
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]
    plt.figure(figsize=(10,10))
    plt.imshow(img)
    
ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
print(text)
