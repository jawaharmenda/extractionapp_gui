import tkinter as tk
from bs4 import BeautifulSoup
import requests
#from PIL import Image, ImageTk
import pandas as pd
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

window = tk.Tk()

# def km():
#     miles=float(e1_value.get())*1.6
#     t1.insert(END,miles)

def selenium_a():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
    browser=webdriver.Chrome(path, chrome_options=chrome_options)
    return browser

def scrape():
    sel=selenium_a()
    link=e1_value.get().split(",")
    df1=pd.DataFrame(columns=['Details'])
    pos=len(df1)
    for sub_link in link:
        sel.get(sub_link)
        soup=BeautifulSoup(sel.page_source)
        l=[]
        for elem in soup(text=re.compile(r'([\w]+ [\d]{5}([\-]?\d{4})?)|([ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1})|(, [0-9]{6})')):
            l.append(elem.parent.parent)
        l=list(dict.fromkeys(l))
        for i in range(len(l)):
            l1=[]
            l1.append('|'.join(l[i].stripped_strings))
            df1.loc[pos]=l1
            pos+=1
    return t1.insert(END,df1)

def excel():
    sel=selenium_a()
    link=e1_value.get().split(",")
    name=e2_value.get()
    df1=pd.DataFrame(columns=['Details','Input_URL'])
    pos=len(df1)
    for sub_link in link:
        sel.get(sub_link)
        soup=BeautifulSoup(sel.page_source)
        l=[]
        for elem in soup(text=re.compile(r'([\w]+ [\d]{5}([\-]?\d{4})?)|([ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1})|(, [0-9]{6})')):
            l.append(elem.parent.parent)
        l=list(dict.fromkeys(l))
        for i in range(len(l)):
            l1=[]
            l1.append('|'.join(l[i].stripped_strings))
            l1.append(sub_link)
            df1.loc[pos]=l1
            pos+=1
    return df1.to_excel(r'{}.xlsx'.format(name))

window.title("Content Address Scraper v.0.1")
window.geometry("900x600")
# frame = tk.Frame(root, bg='brown')
# frame.pack(fill='both', expand='yes')

b1=Button(window,text='HTML Template', bg="orange", command=scrape)
b1.config( height = 4, width = 40 )
b1.grid(row=0,column=0)

b2=Button(window,text='Export to Excel', bg="orange", command=excel)
b2.config( height = 4, width = 40 )
b2.grid(row=1,column=0)

e1_value=StringVar()
e1=Entry(window,textvariable=e1_value,width=40)
# t = Text(e1, height=10, width=40)
# t.pack()
e1.grid(row=0,column=1)
e1.insert(END,"Enter List of URL's Here")

e2_value=StringVar()
e2=Entry(window,textvariable=e2_value,width=40)
# t = Text(e1, height=10, width=40)
# t.pack()
e2.grid(row=1,column=1)
e2.insert(END,"Enter Output File Name")

# t1=Text(window,height=100,width=100)
# t1.grid(row=3,column=1)
t1 = Text(window)
t1.grid(row=3,column=1)
scroll_y = tk.Scrollbar(window, orient="vertical", command=t1.yview)
scroll_y.grid(row=3,column=1,sticky='nsw')
t1.configure(yscrollcommand=scroll_y.set)

window.mainloop()
