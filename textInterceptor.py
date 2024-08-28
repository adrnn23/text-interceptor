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
    

def setCheckbutton(window, iText, intvar):
    checkbutton = ttk.Checkbutton(window, text = iText, 
                    variable = intvar, onvalue = 1, offvalue = 0).pack(pady=10)
    return checkbutton

# Open file and extract table
def openFileExtractTable():
    filepath = filedialog.askopenfilename(title="Open image")
    if filepath.endswith(('.png', '.jpg', '.jpeg')):
        with open(filepath, 'r') as file:
            tableExtractor.extractTable(filepath)
    elif filepath.endswith(("")):
        return
    else:
        messagebox.showerror("Error.", "Incorrect file type.") 

# Open file and extract text from image
def openFileExtractTextFromImage():
    filepath = filedialog.askopenfilename(title="Open image")
    if filepath.endswith(('.png', '.jpg', '.jpeg')):
        with open(filepath, 'r') as file:
            textExtractor.extractText(filepath)
    elif filepath.endswith(("")):
        return
    else:
        messagebox.showerror("Error.", "Incorrect file type.") 

# Zapis tabelki z obrazu do pliku xlsx
def saveTable(df):
    filepath = filedialog.asksaveasfilename(title="Save converted table", defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx .xls"), ("CSV", ".csv")])
    if filepath:
        if filepath.endswith(".csv"):
            df.to_csv(filepath, index=False, header=False)
        elif(filepath.endswith(".csv")): 
            df.to_excel(filepath, index=False, header=False)
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 

# Save text to file
def saveText(text):
    filepath = filedialog.asksaveasfilename(title="Save converted text", defaultextension=".txt", filetypes=[("Txt files", ".txt")])
    if filepath:
        if filepath.endswith(".txt"):
           with open(filepath, 'w') as file:
            #    report = ReportInfo(filepath)
               file.write(text)
               #file.read()
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 


# class ReportInfo:

#     def countWords(self):
#         with open(self.filepath, 'r') as file:
#             text = file.read()
#             print(self.filepath)
#             self.words = len(text.split())
#             print(self.words)

#     def __init__(self, iFilepath):
#         self.filepath = os.path.normpath(iFilepath)
#         self.name = os.path.split(self.filepath)[1]
#         self.datetime = datetime.datetime.now().ctime()
#         self.words = self.countWords()
        

# Text interceptor main view
class TextInterceptor:

    def __init__(self):
        self.mainWindow = setMainWindow()
        self.Checkbutton1 = IntVar()
        self.tabControl = ttk.Notebook(self.mainWindow)

        self.mainPage = ttk.Frame(self.tabControl) 
        self.optionsPage = ttk.Frame(self.tabControl) 

        self.tabControl.add(self.mainPage, text ='Main') 
        self.tabControl.add(self.optionsPage, text ='Options') 
        self.tabControl.pack(expand = 1, fill ="both") 
    
        setTitleLabel(self.mainPage, "Text Interceptor 1.0")
        setButton(self.mainPage, openFileExtractTextFromImage, "Extract text from image")
        setButton(self.mainPage, openFileExtractTextFromImage, "Extract text from video")
        setButton(self.mainPage, openFileExtractTable, "Extract table from image")
        setButton(self.mainPage, self.mainWindow.destroy, "Quit")

        setCheckbutton(self.optionsPage,"Generate raport after text conversion", self.Checkbutton1)
        setButton(self.optionsPage, self.mainWindow.destroy, "Quit")
        self.mainWindow.mainloop()

if __name__ == '__main__':
    ti = TextInterceptor()