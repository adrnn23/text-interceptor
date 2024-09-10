from tkinter import *
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter import messagebox 
import tableExtractor
import textExtractor
import os
import datetime
import json
from fpdf import FPDF
import informationExtractor
import pyautogui
import cv2
import numpy as np
import time
import pyperclip

# Main window configuration
def setMainWindow():
    mainWindow = Tk()
    mainWindow.geometry('700x400')
    mainWindow.title("Text Interceptor 1.0")
    mainWindow.resizable(True,True)
    return mainWindow

# Title label configuration
def setTitleLabel(window, iText):
    title = StringVar()
    title.set(iText)
    label = Label(window, textvariable=title, justify=CENTER, font=("Arial, 16"))
    label.pack(pady=10)
    return label

# Label configuration
def setTextLabel(window, iText):
    text = StringVar()
    text.set(iText)
    label = Label(window, textvariable=text, justify=CENTER, font=("Arial, 10"))
    label.pack(pady=10)
    return label

# Button configuration
def setButton(window, iCommand, iText):
    return ttk.Button(window, text=iText,command=iCommand, width=30, cursor="hand2").pack(pady=8)
    
# Checkbutton configuration
def setCheckbutton(window, iText, intvar):
    checkbutton = ttk.Checkbutton(window, text = iText, 
                    variable = intvar, onvalue = 1, offvalue = 0).pack(pady=8)
    return checkbutton

# Radiobutton configuration
def setRadiobutton(window, intvar):
    filetypes = {
        "TXT" : "1", 
        "PDF" : "2", 
        } 
    
    for (filetype, value) in filetypes.items(): 
        Radiobutton(window, text = filetype, variable = intvar, value = value).pack() 

# Class for current application settings
class Settings:
    def __init__(self):
        self.settingsPath =  r"" + os.getcwd() + "\\settings.json"
        self.jsonSettings = ""

        try:
            with open(self.settingsPath) as jsonFile:
                self.jsonSettings = json.load(jsonFile)
            
            self.generateReports = int(self.jsonSettings["generateReports"])
            self.langPol = int(self.jsonSettings["langPol"])
            self.filetype = int(self.jsonSettings["filetype"])

        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", e)


# ReportInfo class maintains data about image to text conversion (filename, conversion date, number of words, 5 most common words in text)
class ReportInfo:
    # Find 5 most common words in text
    def mostCommonWords(self, iText):
        try:
            if (iText is not None and iText != ""):
                text = iText.split()
                uniqueWords  = []
                for t in text:
                    if(len(text)>0):
                        uniqueWords.append((text.count(t), t))
                        number = text.count(t)
                        for _ in range(number):
                            text.remove(t)
                uniqueWords.sort(key=lambda tuple: tuple[0], reverse=True) # Sort by number of occurrences
                return uniqueWords[0:5] # Return 5 most common words in text
            else:
                return []
        except Exception as e:
            messagebox.showerror("Error", e) 
            return []

    def __init__(self, iFilepath, iText):
        self.filename = os.path.split(iFilepath)[1]
        self.datetime = datetime.datetime.now()
        self.wordsCount = len(iText.split())
        self.charsCount = len(iText)
        self.mostCommonWordsCount = self.mostCommonWords(iText)

    # Report generating
    def generateReport(self):
        reportWindow = Tk()
        reportWindow.geometry('380x260')
        reportWindow.title(f"Report of {self.filename}")
        reportWindow.resizable(False,False)
        textWidget = Text(reportWindow, height=50, width=50)
        textWidget.pack()

        wordsWithNumbers = ""
        for word in self.mostCommonWordsCount:
            wordsWithNumbers += str(word[1]) + "(" + str(word[0]) + ")" + "\n"

        textWidget.insert(INSERT, f"Filename: {self.filename} \nDatetime: {str(self.datetime)[:-7]} \nWords: {self.wordsCount} \nNumber of chars: {self.charsCount} \nThe most common words: {wordsWithNumbers}")  
        reportWindow.mainloop()

# Link window configuration
def showLinkFromQR(link):
    linkWindow = Tk()
    linkWindow.geometry('380x40')
    linkWindow.title("Link from QR")
    linkWindow.resizable(False,False)
    textWidget = Text(linkWindow, height=30, width=50)
    textWidget.pack()
    textWidget.insert(INSERT, link)
    pyperclip.copy(str(link))
    return linkWindow


# Main class TextInterceptor 
class TextInterceptor:
    def __init__(self):
        self.textExtractor = textExtractor.TextExtractor()
        self.tableExtractor = tableExtractor.TableExtractor()
        self.informationExtractor = informationExtractor.InformationExtractor()
        self.settings = Settings()

        self.mainWindow = setMainWindow()
        self.initVariables()
        self.readSettings()
        self.screenshot = []

        self.createTabs()
        self.createMainPage()
        self.createOtherPage()
        self.createOptionsPage()
        self.createHelpPage()

        self.mainWindow.mainloop()

    def initVariables(self):
        self.CheckbuttonReports = IntVar(value=self.settings.generateReports)
        self.CheckbuttonLangPol = IntVar(value=self.settings.langPol)
        self.RadiobuttonFiletype = IntVar(value=self.settings.filetype)

    def createTabs(self):
        self.tabControl = ttk.Notebook(self.mainWindow)
        self.mainPage = ttk.Frame(self.tabControl)
        self.otherPage = ttk.Frame(self.tabControl)
        self.optionsPage = ttk.Frame(self.tabControl)
        self.helpPage = ttk.Frame(self.tabControl)


        self.tabControl.add(self.mainPage, text='Main')
        self.tabControl.add(self.otherPage, text='Other')
        self.tabControl.add(self.optionsPage, text='Options')
        self.tabControl.add(self.helpPage, text='Help')
        self.tabControl.pack(expand=1, fill="both")

    def createMainPage(self):
        setTitleLabel(self.mainPage, "Text Interceptor 1.0")
        setButton(self.mainPage, self.extractTextFromScreenshot, "Extract text from screenshot")
        setButton(self.mainPage, self.extractTextFromImage, "Extract text from image")
        setButton(self.mainPage, self.extractTextFromVideo, "Extract text from video")
        setButton(self.mainPage, self.extractTableFromImage, "Extract table from image")
        setButton(self.mainPage, self.mainWindow.destroy, "Quit")

    def createOtherPage(self):
        setTitleLabel(self.otherPage, "Other functionalities")
        setButton(self.otherPage, self.extractInformation, "Extract information from text")
        setButton(self.otherPage, self.extractQRCodeFromImage, "Read QR code")
        setButton(self.otherPage, self.mainWindow.destroy, "Quit")

    def createOptionsPage(self):
        setTitleLabel(self.optionsPage, "Options")
        setCheckbutton(self.optionsPage, "Generate report after text conversion", self.CheckbuttonReports)
        setCheckbutton(self.optionsPage, "OCR works with Polish", self.CheckbuttonLangPol)
        setTextLabel(self.optionsPage, "Save converted text as:")
        setRadiobutton(self.optionsPage, self.RadiobuttonFiletype)
        setButton(self.optionsPage, self.saveSettings, "Save settings")

    def createHelpPage(self):
        setTitleLabel(self.helpPage, "Help")
        helpDescription = "1. To close the window displaying the image, press Q. \n" 
        helpDescription += "2. Extract text from screenshot - screenshot is taken with the press \nof a button and allows the user to cut out fragment of the image. \n"
        helpDescription += "3. Extract information uses txt files to analyze and get information. \n"
        helpDescription += "4. Rest of functions takes image file as a source. \n"
        helpDescription += "5. Read QR code - give an image of QR code and obtain link to website. \n"
        helpDescription += "6. After changing the settings, you must save settings to use them in program."
        textWidget = Text(self.helpPage, height=800, width=400)
        textWidget.pack()
        textWidget.insert(INSERT, helpDescription )

    # Read settings from Settings class
    def readSettings(self):
        self.CheckbuttonReports = IntVar(value=self.settings.generateReports)
        self.CheckbuttonLangPol = IntVar(value=self.settings.langPol)
        self.RadiobuttonFiletype = IntVar(value=self.settings.filetype)

    # Save current application settings
    def saveSettings(self):
        settings = {
            "generateReports" : str(self.CheckbuttonReports.get()),
            "langPol" : str(self.CheckbuttonLangPol.get()),
            "filetype" : str(self.RadiobuttonFiletype.get()) 
        }

        with open(self.settings.settingsPath, 'w') as jsonFile:
            json.dump(settings, jsonFile)

    def openFile(self, title, filetypes):
        try:
            filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
            if not filepath:
                return None
            for filetype in filetypes:
                if filepath.endswith(filetype[1]):
                    return filepath
            messagebox.showwarning("Warning", "Incorrect file type.")
            return None
        except Exception as e:
            messagebox.showerror("Error", e)
            return None

    def extractTextFromScreenshot(self):
        try:
            self.mainWindow.wm_iconify()
            time.sleep(0.5)
            self.screenshot = pyautogui.screenshot()
            screenshot_np = np.array(self.screenshot)

            # Color conversion from RGB TO BGR
            screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            text = self.textExtractor.extract(screenshot, 'extractText')
                
            if text:
                self.saveText(text)
            else:
                messagebox.showwarning("Warning", "No text found in the screenshot.")

        except Exception as e:
            messagebox.showerror("Error", e) 

    def extractInformation(self):
        filepath = self.openFile("Open file", [("Text files", ('.txt'))])
        if filepath:
            self.informationExtractor.getInformation(filepath)

    def extractTableFromImage(self):
        filepath = self.openFile("Open image", [("Image files", ('.png', '.jpg', '.jpeg'))])
        if filepath:   
            df = self.tableExtractor.extractTable(filepath)
            if df is not None:
                self.saveTable(df)
            else:
                messagebox.showwarning("Warning", "No table found in the image.")

    def extractTextFromImage(self):
        filepath = self.openFile("Open image", [("Image files", ('.png', '.jpg', '.jpeg'))])
        if filepath:
            image = cv2.imread(filepath)
            if image is None:
                messagebox.showerror("Error", f"Loading file error: {filepath}")
                return  
            text = self.textExtractor.extract(image, "extractText")
            if text:
                self.saveText(text)
            else:
                messagebox.showwarning("Warning", "No text found in the image.")

    # Function to implement
    def extractTextFromVideo(self):
        try:
            messagebox.showinfo("Info", "Function is not implemented.")
        except Exception as e:
            messagebox.showerror("Error", e) 


    # Function to implement
    def extractQRCodeFromImage(self):
        filepath = self.openFile("Open image", [("Image files", ('.png', '.jpg', '.jpeg'))])
        if filepath:
            image = cv2.imread(filepath)
            if image is None:
                messagebox.showerror("Error", f"Loading file error: {filepath}")
                return  
            link = self.textExtractor.extract(image, "extractQRCode")
            if link is not None:
                linkWindow = showLinkFromQR(link)
                linkWindow.mainloop()
            else:
                messagebox.showwarning("Warning", "No text found in the image.")

    def saveText(self, text):
        settingsPath = r"" + os.getcwd() + "\\settings.json"
        jsonSettings = ""

        with open(settingsPath) as jsonFile:
            jsonSettings = json.load(jsonFile)

        filetype = int(jsonSettings["filetype"])

        if(filetype == 1):
            self.saveToTxtFile(text)
        elif(filetype == 2):
            self.saveToPdfFile(text)
        else:
            messagebox.showwarning("Warning", "Incorrect file type.")

    def saveToTxtFile(self, text):
        try:
            filepath = filedialog.asksaveasfilename(title="Save converted text", defaultextension=".txt", filetypes=[("TXT files", ".txt")])
            if filepath == "":
                return
            if not filepath.endswith(".txt"):
                messagebox.showwarning("Warning", "Incorrect file type.")
                return
            
            with open(filepath, 'w+') as file:
                file.write(text)
            if self.CheckbuttonReports.get() == 1:
                report = ReportInfo(filepath, text)
                report.generateReport()

        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

    def saveToPdfFile(self, text):
        try:
            filepath = filedialog.asksaveasfilename(title="Save converted text", defaultextension=".pdf", filetypes=[("PDF files", ".pdf")]) 
            if filepath:
                pdf = FPDF()
                pdf.add_font('DejaVu', '', r"" + os.getcwd() + "\\dejavu-sans\\ttf\\DejaVuSansCondensed.ttf", uni=True)
                pdf.set_font('DejaVu', '', 10)
                pdf.add_page()
                pdf.multi_cell(0, 4, text)
                pdf.output(filepath)
            if self.CheckbuttonReports.get() == 1:
                report = ReportInfo(filepath, text)
                report.generateReport()

        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

    def saveTable(self, df):
        try:
            filepath = filedialog.asksaveasfilename(title="Save converted table", defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx .xls"), ("CSV", ".csv")])
            if filepath == "":
                return
            if (filepath.endswith(".xlsx") or filepath.endswith(".xls")):
                df.to_excel(filepath, index=False, header=False)
            elif filepath.endswith(".csv"):
                df.to_csv(filepath, index=False, header=False)
            else:
                messagebox.showwarning("Warning", "Incorrect file type.")
                return

        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

if __name__ == '__main__':
    textInterceptor = TextInterceptor()