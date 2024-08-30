from tkinter import *
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter import messagebox 
import tableExtractor
import textExtractor
import os
import datetime
import json

# Main window configuration
def setMainWindow():
    mainWindow = Tk()
    mainWindow.geometry('400x340')
    mainWindow.title("Text Interceptor 1.0")
    mainWindow.resizable(False,False)
    return mainWindow

# Label configuration
def setTitleLabel(window, text):
    title = StringVar()
    title.set(text)
    label = Label(window, textvariable=title, justify=CENTER, font=("Arial, 16"))
    label.pack(pady=10)
    return label

# Button configuration
def setButton(window, iCommand, iText):
    return ttk.Button(window, text=iText,command=iCommand, width=30, cursor="hand2").pack(pady=10)
    
# Checkbutton configuration
def setCheckbutton(window, iText, intvar):
    checkbutton = ttk.Checkbutton(window, text = iText, 
                    variable = intvar, onvalue = 1, offvalue = 0).pack(pady=10)
    return checkbutton

# Class for current application settings
class Settings:
    def __init__(self):
        self.settingsPath = r"" + os.getcwd() + "\\settings.json"
        self.jsonSettings = ""

        # print(self.settingsPath)

        with open(self.settingsPath) as jsonFile:
            self.jsonSettings = json.load(jsonFile)
        
        self.generateReports = int(self.jsonSettings["generateReports"])
        self.langPol = int(self.jsonSettings["langPol"])

# Link window configuration
def showLinkFromQR(link):
    linkWindow = Tk()
    linkWindow.geometry('380x40')
    linkWindow.title("Link from QR")
    linkWindow.resizable(False,False)
    textWidget = Text(linkWindow, height=30, width=50)
    textWidget.pack()
    textWidget.insert(INSERT, link)  
    return linkWindow

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
        self.mostCommonWordsCount = self.mostCommonWords(iText)

    # Report generating
    def generateReport(self):
        reportWindow = Tk()
        reportWindow.geometry('380x180')
        reportWindow.title(f"Report of {self.filename}")
        reportWindow.resizable(False,False)
        textWidget = Text(reportWindow, height=50, width=50)
        textWidget.pack()

        wordsWithNumbers = ""
        for word in self.mostCommonWordsCount:
            wordsWithNumbers += str(word[1]) + "(" + str(word[0]) + ")" + "\n"

        textWidget.insert(INSERT, f"Filename: {self.filename} \nDatetime: {str(self.datetime)[:-7]} \nWords: {self.wordsCount} \nThe most common words: {wordsWithNumbers}")  
        reportWindow.mainloop()

# Main class TextInterceptor 
class TextInterceptor:
    def __init__(self):
        self.textExtractor = textExtractor.TextExtractor()
        self.tableExtractor = tableExtractor.TableExtractor()
        self.settings = Settings()

        self.mainWindow = setMainWindow()
        self.CheckbuttonReports = IntVar()
        self.CheckbuttonLangPol = IntVar()

        self.readSettings()

        self.tabControl = ttk.Notebook(self.mainWindow)
        self.mainPage = ttk.Frame(self.tabControl) 
        self.optionsPage = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.mainPage, text='Main') 
        self.tabControl.add(self.optionsPage, text='Options') 
        self.tabControl.pack(expand=1, fill="both") 

        # Text interceptor main page
        setTitleLabel(self.mainPage, "Text Interceptor 1.0")
        setButton(self.mainPage, self.extractTextFromImage, "Extract text from image")
        setButton(self.mainPage, self.extractTextFromVideo, "Extract text from video")
        setButton(self.mainPage, self.extractTableFromImage, "Extract table from image")
        setButton(self.mainPage, self.extractQRCodeFromImage, "Read QR code")
        setButton(self.mainPage, self.mainWindow.destroy, "Quit")

        # Options page
        setTitleLabel(self.optionsPage, "Options")
        setCheckbutton(self.optionsPage, "Generate report after text conversion", self.CheckbuttonReports)
        setCheckbutton(self.optionsPage, "OCR works with Polish", self.CheckbuttonLangPol)
        setButton(self.optionsPage, self.saveSettings, "Save settings")
        setButton(self.optionsPage, self.mainWindow.destroy, "Quit")

        self.mainWindow.mainloop()

    # Read settings from Settings class
    def readSettings(self):
        self.CheckbuttonReports = IntVar(value=self.settings.generateReports)
        self.CheckbuttonLangPol = IntVar(value=self.settings.langPol)

    # Save current application settings
    def saveSettings(self):
        generateReports = self.CheckbuttonReports
        langPol = self.CheckbuttonLangPol

        settings = {
            "generateReports" : str(generateReports.get()),
            "langPol" : str(langPol.get())
        }

        with open(self.settings.settingsPath, 'w') as jsonFile:
            json.dump(settings, jsonFile)

    def extractTableFromImage(self):
        try:
            filepath = filedialog.askopenfilename(title="Open image")
            if filepath == "":
                return
            if not filepath.endswith(('.png', '.jpg', '.jpeg')):
                messagebox.showwarning("Warning", "Incorrect file type.")
                return
            
            df = self.tableExtractor.extractTable(filepath)
            if df is not None:
                self.saveTable(df)
            else:
                messagebox.showwarning("Warning", "No table found in the image.")

        except FileNotFoundError as e:
            messagebox.showerror("Error", e) 
        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

    def extractTextFromImage(self):
        try:
            filepath = filedialog.askopenfilename(title="Open image")
            if filepath == "":
                return
            if not filepath.endswith(('.png', '.jpg', '.jpeg')):
                messagebox.showwarning("Warning", "Incorrect file type.")
                return

            text = self.textExtractor.extract(filepath, "extractText")
            if text is not None:
                self.saveText(text)
            else:
                messagebox.showwarning("Warning", "No text found in the image.")

        except FileNotFoundError as e:
            messagebox.showerror("Error", e) 
        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

    # Function to implement
    def extractTextFromVideo(self):
        try:
            messagebox.showinfo("Info", "Function is not implemented.")
        except Exception as e:
            messagebox.showerror("Error", e) 


    # Function to implement
    def extractQRCodeFromImage(self):
        try:
            filepath = filedialog.askopenfilename(title="Open image")
            if filepath == "":
                return
            if not filepath.endswith(('.png', '.jpg', '.jpeg')):
                messagebox.showwarning("Warning", "Incorrect file type.")
                return
            
            link = self.textExtractor.extract(filepath, "extractQRCode")
            if link is not None:
                linkWindow = showLinkFromQR(link)
                linkWindow.mainloop()
            else:
                messagebox.showwarning("Warning", "No text found in the image.")

        except FileNotFoundError as e:
            messagebox.showerror("Error", e) 
        except IOError as e:
            messagebox.showerror("Error", e) 
        except Exception as e:
            messagebox.showerror("Error", e) 

    def saveText(self, text):
        try:
            filepath = filedialog.asksaveasfilename(title="Save converted text", defaultextension=".txt", filetypes=[("Txt files", ".txt")])
            if filepath == "":
                return
            if not filepath.endswith(".txt"):
                messagebox.showwarning("Warning", "Incorrect file type.")
                return
            
            with open(filepath, 'w+') as file:
                file.write(text)
                if self.CheckbuttonReports.get() == 1:
                    report = ReportInfo(filepath, text)
                    # print(report.filename, report.datetime, report.wordsCount, report.mostCommonWordsCount)
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