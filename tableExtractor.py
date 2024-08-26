import pytesseract
import numpy as np
import cv2
import pandas as pd
import imutils
import textInterceptor as ti
from tkinter import messagebox 

# Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Rgb to grayscale 
def convertToGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Image processing, grayscale conversion, thresholding
def preProcessImage(image):
    grayImage = convertToGrayscale(image)
    grayImage = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.bitwise_not(grayImage)

# Function return true if analyzed area is probably table
def isTable(contours, imageArea, minContours=4, minCellArea=20):

    if len(contours) < minContours:
        print("Contours < 4")
        return False

    cellAreas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > minCellArea]
    
    if len(cellAreas) < minContours:
        print("len(cellAreas) < minContours")
        return False

    return True

# Table structure detection, table's horizontal and vertical lines merging
def detectTableStructure(image):
    rectangles = []

    potentialTable = preProcessImage(image)

    dilateKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    potentialTable = cv2.dilate(potentialTable, kernel=dilateKernel, iterations=1)

    # cv2.imshow("Processed image", potentialTable)
    # cv2.waitKey(0)

    # Detecting vertical and horizontal lines in image
    hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (image.shape[1] // 8, 1))
    hLines = cv2.erode(potentialTable, hKernel, iterations=2)
    hLines = cv2.dilate(hLines, hKernel, iterations=2)

    vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, image.shape[0] // 8))
    vLines = cv2.erode(potentialTable, vKernel, iterations=2)
    vLines = cv2.dilate(vLines, vKernel, iterations=2)

    combinedLines = cv2.addWeighted(hLines, 0.5, vLines, 0.5, 0.0)
    combinedLines = cv2.dilate(combinedLines, dilateKernel, iterations=2)
    # cv2.imshow("Combined lines", combinedLines)
    # cv2.waitKey(0)

    # Finding all contours of potential table 
    contours, _ = cv2.findContours(combinedLines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Finding all rectangles in contours
    for contour in contours:
        length = cv2.arcLength(contour, True) #Calculate perimeter of contour
        approx = cv2.approxPolyDP(contour, 0.02 * length, True) #approxPolyDP simplifies the shape of contour
        #If approx has 4 vertices then approx is possible rectangle
        if len(approx) == 4:
            rectangles.append(approx)

    # Finding biggest rectangle - shape of table
    maxRectangle = 0 
    maxContour = None
    for rectangle in rectangles:
        if(cv2.contourArea(rectangle)>maxRectangle):
            maxRectangle = cv2.contourArea(rectangle)
            maxContour = rectangle

    if maxContour is not None:
        x, y, w, h = cv2.boundingRect(maxContour)
        potentialTable = combinedLines[y:y+h, x:x+w]
        potentialTableImage = image[y:y+h, x:x+w]

        contours, _ = cv2.findContours(potentialTable, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if(isTable(contours, image.shape[0]*image.shape[1], 4, 20)):
            return True, contours, potentialTableImage

    return False, [], []

# Table extraction, reading text from cells and saving it in DataFrame
def extractTable(inputPath):

    image = cv2.imread(inputPath)
    if image is None:
        messagebox.showinfo("Result.", f"Loading file error: {inputPath}") 
        return

    isTable, contours, image = detectTableStructure(image)
    
    if isTable:
        messagebox.showinfo("Result.", "Table is detected.") 
        data = []
        for i in range(len(contours)-1):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w > 10 and h > 10:
                cell = image[y:y+h, x:x+w]
                text = pytesseract.image_to_string(cell, config='--psm 6')
                data.append((y, x, text.strip()))

        # Adding cells to table 
        rows = {}
        for y, x, text in data:
            if y not in rows:
                rows[y] = {}
            rows[y][x] = text

        table_list = []
        for y in sorted(rows.keys()):
            row = rows[y]
            table_list.append([row[x] if x in row else '' for x in sorted(row.keys())])

        df = pd.DataFrame(table_list)
        ti.saveXlsx(df)
    else:
        messagebox.showinfo("Result.", "Image without table.") 