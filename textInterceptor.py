from tkinter import *
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter import messagebox 
import tableExtractor
import textExtractor
import numpy as np
import os
import datetime

# Main window configuration
def setMainWindow():
    mainWindow = Tk()
    mainWindow.geometry('400x300')
    mainWindow.title("Text Interceptor 1.0")
    mainWindow.resizable(False,False)
    return mainWindow

# Label configuration
def setTitleLabel(window, text):
    title = StringVar()
    title.set(text)
    label = ttk.Label(window, textvariable=title, anchor=CENTER, justify=CENTER, width=30)
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

# ReportInfo class maintains data about image to text conversion
class ReportInfo:
    def __init__(self, iFilepath, iText):
        self.name = os.path.split(iFilepath)[1]
        self.datetime = datetime.datetime.now()
        self.words = len(iText.split())

# Main class TextInterceptor 
class TextInterceptor:
    def __init__(self):
        self.textExtractor = textExtractor.TextExtractor()
        self.tableExtractor = tableExtractor.TableExtractor()
        self.mainWindow = setMainWindow()
        self.Checkbutton1 = IntVar()
        self.tabControl = ttk.Notebook(self.mainWindow)

        self.mainPage = ttk.Frame(self.tabControl) 
        self.optionsPage = ttk.Frame(self.tabControl) 

        self.tabControl.add(self.mainPage, text='Main') 
        self.tabControl.add(self.optionsPage, text='Options') 
        self.tabControl.pack(expand=1, fill="both") 

        setTitleLabel(self.mainPage, "Text Interceptor 1.0")
        setButton(self.mainPage, self.extractTextFromImage, "Extract text from image")
        setButton(self.mainPage, self.extractTextFromVideo, "Extract text from video")
        setButton(self.mainPage, self.extractTableFromImage, "Extract table from image")
        setButton(self.mainPage, self.mainWindow.destroy, "Quit")

        setCheckbutton(self.optionsPage, "Generate report after text conversion", self.Checkbutton1)
        setButton(self.optionsPage, self.mainWindow.destroy, "Quit")
        self.mainWindow.mainloop()

    def extractTableFromImage(self):
        filepath = filedialog.askopenfilename(title="Open image")
        if filepath.endswith(('.png', '.jpg', '.jpeg')):
            df = self.tableExtractor.extractTable(filepath)
            if df is not None:
                self.saveTable(df)
        elif filepath == "":
            return
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 

    def extractTextFromImage(self):
        filepath = filedialog.askopenfilename(title="Open image")
        if filepath.endswith(('.png', '.jpg', '.jpeg')):
            text = self.textExtractor.extractText(filepath)
            if text is not None:
                self.saveText(text)
        elif filepath == "":
            return
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 

    def extractTextFromVideo(self):
        messagebox.showinfo("Info", "Function is not implemented.")

    def saveText(self, text):
        filepath = filedialog.asksaveasfilename(title="Save converted text", defaultextension=".txt", filetypes=[("Txt files", ".txt")])
        if filepath.endswith(".txt"):
            with open(filepath, 'w') as file:
                file.write(text)
                if self.Checkbutton1.get() == 1:
                    report = ReportInfo(filepath, text)
                    print(report.name, report.datetime, report.words)
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 

    def saveTable(self, df):
        filepath = filedialog.asksaveasfilename(title="Save converted table", defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx .xls"), ("CSV", ".csv")])
        if filepath:
            if filepath.endswith(".csv"):
                df.to_csv(filepath, index=False, header=False)
            elif(filepath.endswith(".xlsx") or filepath.endswith(".xls")): 
                df.to_excel(filepath, index=False, header=False)
            else:
                messagebox.showerror("Error.", "Incorrect file type.") 

if __name__ == '__main__':
    textInterceptor = TextInterceptor()