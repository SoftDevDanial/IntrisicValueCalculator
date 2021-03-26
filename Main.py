"""
    Programmer: Mohd Danial Saufi Bin Ezani
    Date: 7/15/2020
    Program Aim: Main GUI for the program

"""
import tkinter as tk
from tkinter import ttk 
import IntrisicValScript as ivs
import pandas as pd
from tkinter import messagebox

class MainApp():

    #### Initializiation ####
    def __init__(self):
        pass
    #### First Tab ####
    def firstTab(self, parent):

        self.gtick = []
        self.fileName = '../IntrisicValueCalculator/Saved Ticks DO NOT DELETE'
        try:
            f_read = open( self.fileName , 'r')
            self.gtick = f_read.read().splitlines()
            f_read.close()
            print(self.gtick)
        except ValueError:
            print("File Cannot Be Read[No file found or file corrupted]")
        

        #### Styling ####
        style = ttk.Style()
        style.theme_use('xpnative') #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

        #### FRAME ####
        frame1 = tk.LabelFrame(parent , text = "Sidebar")
        frame2 = tk.LabelFrame(parent , text = "Table")
        frame3 = tk.LabelFrame(parent , text = "Inputs")
        frame1.pack(fill = "both" , expand = "yes" ,padx = 20 , pady = 5)
        frame2.pack(fill = "both" , expand = "yes" ,padx = 20 , pady = 0)
        frame3.pack(fill = "x" , expand = "yes" ,padx = 20 , pady = 5)

        #### TABLE ####
        trv = ttk.Treeview(frame2 , columns = (1,2,3,4,5,6) , show = "headings" , height = "10" )
        trv.grid(row = 0 , column = 0)
        trv.heading(1, text = "Symbol")
        trv.heading(2, text = "Outstanding Shares")
        trv.heading(3, text = "EPS 5 Years")
        trv.heading(4, text = "Discount Rate")
        trv.heading(5, text = "Last Close Price")
        trv.heading(6, text = "Current Intrisic Value")
        self.Data(trv)
        trvScroll = ttk.Scrollbar(frame2 , orient = "vertical" , command = trv.yview)
        trv.configure(yscroll = trvScroll.set)
        trvScroll.grid(row = 0 , column = 6 , stick = "ns")
        
        #Price Valuation - PEG RATIO , Discounted Cash Flow from Operations, Discounted Net Income , Price to Book Value , Price to Sales Growth ratio
        #### Inputs ####
        input_field = tk.Entry(frame3)
        input_field.pack(side = "left" , padx = 20 , pady = 5 )
        enter = tk.Button(frame3, text = "Search" , command = lambda: self.getData(input_field.get().upper() , trv))
        enter.pack(side = "left" ,padx = 20 , pady = 5)
        self.var = tk.StringVar()
        label = tk.Label( frame3, textvariable=self.var , foreground="red")
        label.pack(side = "left" ,padx = 20 , pady = 5)

    #### Second Tab ####
    def secondTab(self, parent):

        #### Frame ####
        frame_1 = tk.LabelFrame(parent , text = "Test11")
        frame_2 = tk.LabelFrame(parent , text = "TEST")
        frame_1.pack(fill = "both" , expand = "yes" ,padx = 20 , pady = 5)
        frame_2.pack(fill = "both" , expand = "yes" ,padx = 20 , pady = 0)


    #### Save All Files ####
    def save(self):
        try:
            f_write = open(self.fileName , 'w')
            for i in range(len(self.gtick)):
                f_write.write(self.gtick[i] + '\n')
            f_write.close()
        except ValueError:
            print("Unable to Write to File[Missing/Corrupted File]")
    

    #### Update Rows ####
    def Data(self, parent):
        myList = self.gtick
        df = ivs.IntrisicValScript(myList).calcIntVal()
        df_col = df.columns.values.tolist()
        for row in parent.get_children():
            parent.delete(row)
        for i in range(len(myList)):
            value = []
            for x in range(len(df_col)):
                value.append(df[df_col[x]][i])
            parent.insert('' , x , values = (value))

    def getData(self , tick , parent):
        dupl = False
        for i in range(len(self.gtick)):
            if tick ==self. gtick[i]:
                dupl = True
        if dupl == False:
            self.gtick.append(tick)
            self.save()
            self.Data(parent)
        elif dupl == True:
            self.var.set("Duplicate Stock Ticker")


def on_close(window , root):
    close = messagebox.askokcancel("Close", "Would you like to close the program?")
    if close:
        root.save()
        window.destroy()
        

def main():
    #### Initialize Tkinter ####
    window = tk.Tk()
    window.title("GUI PYTHON TEST")
    window.geometry("1280x800")

    #### Tab Frames ####
    tab_NB = ttk.Notebook(window)
    tab_NB.pack()
    tab_1_frame = tk.Frame(tab_NB , width = "1280" , height = "800")
    tab_1_frame.pack(fill = "both"  , expand = "yes")
    tab_2_frame = tk.Frame(tab_NB, width = "1280" , height = "800")
    tab_2_frame.pack(fill = "both" , expand = "yes")
    tab_NB.add(tab_1_frame , text = "Information")
    tab_NB.add(tab_2_frame , text = "Investing")
    #### Run App ####
    App = MainApp()
    App.firstTab(tab_1_frame)
    App.secondTab(tab_2_frame)
    window.protocol("WM_DELETE_WINDOW",  lambda:on_close(window , App))
    window.mainloop()

if __name__ == '__main__':
    main()



