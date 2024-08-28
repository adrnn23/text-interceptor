import pytesseract
import cv2
import textInterceptor as ti
from tkinter import messagebox 

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

x0, y0, x1, y1 = 1, 1, 1, 1
clicked = False

# Get mouse position at LBUTTONDOWN and LBUTTONUP
def getMouseClickPosition(event, x, y, flags, param):
    global x0, y0, x1, y1, clicked
    
    if event == cv2.EVENT_LBUTTONDOWN:
        x0, y0 = x, y
        clicked = False
    elif event == cv2.EVENT_LBUTTONUP:
        x1, y1 = x, y
        clicked = True

# Extract text from image 
def extractText(filepath):
    global clicked
    image = cv2.imread(filepath)
    if image is None:
        messagebox.showerror("Error.", f"Loading file error: {filepath}") 
        return
    
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', getMouseClickPosition)
    while True:
        if clicked:
            # Cropping the image with text, mouse position at LBUTTONDOWN and LBUTTONUP is used
            img = image[y0:y1, x0:x1]
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   
            text = pytesseract.image_to_string(gray, config='-l eng+pol --psm 6')
            clicked = False
            if text is not None:
                ti.saveText(text)
                cv2.destroyAllWindows()

        # Wait for key, if q is pressed then close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return