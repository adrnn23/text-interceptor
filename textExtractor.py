import cv2
from tkinter import messagebox
from screeninfo import get_monitors
import pytesseract
from pyzbar.pyzbar import decode
import json
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Return lang settings from settings.json
def returnLang():
    settingsPath = r"" + os.getcwd() + "\\settings.json"
    jsonSettings = ""

    with open(settingsPath) as jsonFile:
        jsonSettings = json.load(jsonFile)

    langPol = int(jsonSettings["langPol"])

    if(langPol == 1):
        lang = 'eng+pol'
    else:
        lang = 'eng'
    return lang

def imageToString(cell):
    langFromJson = returnLang()
    return pytesseract.image_to_string(cell, lang = langFromJson, config='--psm 6')

# Function used to resize image if it is too big to display
def resizeImage(image):
    scaleRatio = 0

    monitor = get_monitors()
    if(monitor[0].width==1920 and monitor[0].height==1080):
        # Optimal image size for 1920x1080
        height = 812
        width = 1524

        if(image.shape[1] > 1524 and image.shape[0] < 812):
            width = 1524
            scaleRatio = width / image.shape[1]
            height = int(image.shape[0]*scaleRatio)
        elif(image.shape[1] < 1524 and image.shape[0] > 812):
            height = 812
            scaleRatio = height / image.shape[0]
            width = int(image.shape[1]*scaleRatio)
        else:
            height = 812
            width = 1524
        
        # print(image.shape[0], image.shape[1])
        # print(height, width)
        image = cv2.resize(image, (width, height))

    return image

class TextExtractor:
    def __init__(self):
        self.x0, self.y0, self.x1, self.y1 = 1, 1, 1, 1
        self.clicked = False

    # Get mouse position at LBUTTONDOWN and LBUTTONUP
    def getMouseClickPosition(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x0, self.y0 = x, y
            self.clicked = False
        elif event == cv2.EVENT_LBUTTONUP:
            self.x1, self.y1 = x, y
            self.clicked = True
        
    def extract(self, filepath, function):
        try:
            # Load the image
            image = cv2.imread(filepath)
            if image is None:
                messagebox.showerror("Error", f"Loading file error: {filepath}")
                return None

            # Resize the image if it is too big
            if image.shape[0] > 812 or image.shape[1] > 1524:
                image = resizeImage(image)

            cv2.imshow('Image', image)
            cv2.setMouseCallback('Image', self.getMouseClickPosition)

            while True:
                if self.clicked:
                    croppedImage = self.cropImage(image)
                    gray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
                    self.clicked = False 

                    if function == "extractText":
                        return self.extractText(gray)
                    elif function == "extractQRCode":
                        return self.extractQRCode(gray)
                    else:
                        messagebox.showwarning("Warning","Incorrect operation.")
                        return None

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()
            return None
        
        except cv2.error as e:
            messagebox.showerror("OpenCV Error", f"OpenCV error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        cv2.destroyAllWindows()
        return None

    def cropImage(self, image):
        return image[self.y0:self.y1, self.x0:self.x1]

    def extractText(self, grayImage):
        text = imageToString(grayImage)
        if text:
            cv2.destroyAllWindows()
            return text
        return ""

    def extractQRCode(self, grayImage):
        decoded = decode(grayImage)
        cv2.destroyAllWindows()
        if decoded:
            link = decoded[0].data.decode('utf-8')
            if link:
                return link
            else:
                messagebox.showwarning("No link found in QR code.")
        else:
            messagebox.showwarning("No QR code found.")
        return None