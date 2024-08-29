import pytesseract
import cv2
from tkinter import messagebox
import textInterceptor as ti

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

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

    # Extract text from image 
    def extractText(self, filepath):
        try:
            image = cv2.imread(filepath)
            if image is None:
                messagebox.showerror("Error", f"Loading file error: {filepath}")
                return
            
            cv2.imshow('Image', image)
            cv2.setMouseCallback('Image', self.getMouseClickPosition)

            while True:
                if self.clicked:
                    # Cropping the image with text, using mouse position at LBUTTONDOWN and LBUTTONUP
                    img = image[self.y0:self.y1, self.x0:self.x1]
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
                    text = pytesseract.image_to_string(gray, config='-l eng+pol --psm 6')
                    self.clicked = False
                    if text:
                        cv2.destroyAllWindows()
                        return text  

                # Wait for key, if q is pressed then close the window
                if (cv2.waitKey(1) and 0xFF == ord('q')):
                    break

            cv2.destroyAllWindows()
            return None
        
        except Exception as e:
            messagebox.showerror("Error", e) 
            return None