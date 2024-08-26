from tkinter import *
from tkinter import filedialog
from tkinter import messagebox 
import tableExtractor

# Label configuration
def setTitleLabel(window, text):
    title = StringVar()
    title.set(text)
    return Label(window, textvariable=title, anchor=CENTER, 
                 fg="orange", bg="black", justify=CENTER, height=2, width=30, borderwidth=0,
                 font=("Arial", 24), relief='raised').pack(pady=10)

# Button configuration
def setButton(window, iCommand, iText):
    return Button(window, text=iText,command=iCommand, 
           bg='orange', fg='black', font=("Arial", 18), relief='raised', borderwidth=2, 
           activebackground='darkorange', width=30, cursor="hand2").pack(pady=10)
    
# Open file function
def openFile():
    filepath = filedialog.askopenfilename(title="Open image")
    if filepath.endswith(('.png', '.jpg', '.jpeg')):
        with open(filepath, 'r') as file:
            tableExtractor.extractTable(filepath)

# Zapis tabelki z obrazu do pliku xlsx
def saveXlsx(df):
    filepath = filedialog.asksaveasfilename(title="Save Excel file", defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx .xls")])
    if filepath:
        df.to_excel(filepath, index=False, header=False)

# Text interceptor main view
def textInterceptor():
    # main window configuration
    window = Tk()
    window.geometry('600x400')
    window.title("Text Interceptor 1.0")
    window.configure(bg='black')
    window.resizable(False,False)

    setTitleLabel(window, "Text Interceptor 1.0")

    setButton(window, openFile, "Extract text from image")

    setButton(window, openFile, "Extract text from video")

    setButton(window, openFile, "Extract table from image")

    setButton(window, window.destroy, "Quit")

    window.mainloop()

if __name__ == '__main__':
    textInterceptor()