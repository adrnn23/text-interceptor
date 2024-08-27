from tkinter import *
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter import messagebox 
import tableExtractor

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

# Open file function
def openFile():
    filepath = filedialog.askopenfilename(title="Open image")
    if filepath.endswith(('.png', '.jpg', '.jpeg')):
        with open(filepath, 'r') as file:
            tableExtractor.extractTable(filepath)
    elif filepath.endswith(("")):
        return
    else:
        messagebox.showerror("Error.", "Incorrect file type.") 

# Zapis tabelki z obrazu do pliku xlsx
def saveXlsx(df):
    filepath = filedialog.asksaveasfilename(title="Save Excel file", defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx .xls"), ("CSV", ".csv")])
    if filepath:
        if filepath.endswith(".csv"):
            df.to_csv(filepath, index=False, header=False)
        elif(filepath.endswith(".csv")): 
            df.to_excel(filepath, index=False, header=False)
        else:
            messagebox.showerror("Error.", "Incorrect file type.") 

# Text interceptor main view
def textInterceptor():

    mainWindow = setMainWindow()
    Checkbutton1 = IntVar()

    tabControl = ttk.Notebook(mainWindow)
    mainPage = ttk.Frame(tabControl) 
    optionsPage = ttk.Frame(tabControl) 

    tabControl.add(mainPage, text ='Main') 
    tabControl.add(optionsPage, text ='Options') 
    tabControl.pack(expand = 1, fill ="both") 
    
    setTitleLabel(mainPage, "Text Interceptor 1.0")
    setButton(mainPage, openFile, "Extract text from image")
    setButton(mainPage, openFile, "Extract text from video")
    setButton(mainPage, openFile, "Extract table from image")
    setButton(mainPage, mainWindow.destroy, "Quit")

    setCheckbutton(optionsPage,"Generate raport after text conversion", Checkbutton1)
    setButton(optionsPage, mainWindow.destroy, "Quit")
    mainWindow.mainloop()

if __name__ == '__main__':
    textInterceptor()