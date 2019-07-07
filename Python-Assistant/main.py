# import required libraries
from tkinter import ttk
from pycricbuzz import Cricbuzz
from win10toast import ToastNotifier
from tkinter.messagebox import *
from tkinter.filedialog import *
import json
import pytesseract
import os
from mutagen.mp3 import MP3
import threading
from PIL import Image,ImageTk
import random
import wikipedia
import webbrowser
import cv2
from difflib import get_close_matches
from translate import  Translator
from time import strftime,sleep
from  datetime import  *
import  textwrap
from  bbcnews import getweather,NewsFromBBC,searchbooks # get news methods from bbcnews.py
import  backend #get bookstore backend
from google_images_download import google_images_download
from jarvis import * #get voice assistant methods from jarvis.py
from pygame import  mixer

# class for root window
class Window(object):
    def __init__(self,root):
        # Defining root properties
        self.root=root
        self.root.title('R.A.SSISTANT')
        self.root.geometry("540x640+500+5")
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.bind('<Button-1>', self.onclick)
        self.tabControl.pack(expand=1, fill="both")

    # onlclick method for tabs
    def onclick(self,event):
        clicked_tab = self.tabControl.tk.call(self.tabControl._w, "identify", "tab", event.x, event.y)
        active_tab = self.tabControl.index(self.tabControl.select())
        if clicked_tab == 4:
            if active_tab != 4:
                t=threading.Thread(target=self.mythread)
                t.start()

    def mythread(self):
        try:
            voiceassistant.wishMe()
            speak("Jarvis here. Please tell me how may I help you")
        except:
            print("error")

# homepage class
class Homepage:
    def __init__(self,tabControl):
        # add tab
        self.tab1=ttk.Frame(tabControl)
        tabControl.add(self.tab1,text="Home")
        self.mynotifier=Label(self.tab1)
        self.c = Cricbuzz()
        self.matches = self.c.matches()
        self.n=ToastNotifier()
        # create a new frame and pack widgets in it
        self.row1 = Frame(self.tab1, bg="lightyellow")
        #label for displaying clock
        self.clocklbl = Label(self.row1, font=('calibri', 15, 'bold'), fg="blue", bg="lightgreen")
        # weather image
        self.weatherimg = Image.open("images/weatherimg.jpeg")
        # get height and width of image
        wd, ht = self.weatherimg.size
        # resize image
        self.weatherimg = self.weatherimg.resize((wd // 4, ht // 4))
        # convert to tkinter image
        self.render = ImageTk.PhotoImage(self.weatherimg)
        # label to display image
        self.weatherimglbl = Label(self.row1, image=self.render)
        # set image to label
        self.weatherimglbl.image = self.render

        # Get weather of a city entered by user
        self.lblweather = Label(self.row1, text="Today's Weather", font=('calibri', 20, 'bold'))
        self.myweathervar = StringVar()
        # Label to display weather of my city
        self.myweather = Label(self.row1, textvariable=self.myweathervar, bg='lightgray', font=('times', 11, 'bold'))
        # calling getweather method defined in bbcnews
        self.cityweather = getweather("nagpur")
        # set weather details
        self.myweathervar.set(self.cityweather)
        # get weather of any city in the world
        self.getcityweatherlbl = Label(self.row1, text="Get Weather for city :", font=('times', 15, 'bold'))
        self.cityvar = StringVar()
        # entry to accept cityname as input
        self.cityvarentry = Entry(self.row1, textvariable=self.cityvar, font=('times', 15))
        self.showvar = StringVar()
        # label to display weather info
        self.showweatherlbl = Label(self.row1, textvariable=self.showvar, bg='lightpink', font=('times', 10, 'bold'))

        # creating new frame to display news headlines
        self.row7 = Frame(self.tab1)
        self.newslbl = Label(self.row7, text="Headlines for Today:",bg="lightgreen", font=('times', 15, 'bold'))
        self.newstext = Label(self.row7, bg="lightyellow", font=('times', 12), wraplength=530, justify="left")
        self.mytt = threading.Thread(target=self.mynotify)
        self.mytt.daemon=True
        self.mytt.start()

    # define properties of widgets


    def set(self):
        self.cityvarentry.config(bd=5)
        self.cityvarentry.bind("<Return>", self.getcityweather)
        self.getnews()

    # get news
    def getnews(self):
        self.results = NewsFromBBC()
        i = 0
        for ar in self.results:
            ss = str(i + 1) + ". " + ar["title"] + "\n"
            ss = self.newstext.cget("text") + ss
            self.newstext.config(text=ss)
            i += 1

    # getcityweather
    def getcityweather(self,event):
        if self.cityvar.get() == "":
            self.cityvar.set("")
            showerror("Error", "City Not Found \n"
                               "Please enter valid city name")

        else:
            if getweather(self.cityvar.get()) == "N":
                self.cityvar.set("")
                showerror("Error", "City Not Found \n"
                                   "Please enter valid city name")
            else:
                self.showweatherlbl.grid(row=1, column=2, pady="10")
                self.showvar.set(getweather(self.cityvar.get()))
                self.cityvarentry.delete(0, END)

    # method to update time in clock label
    def gettime(self):
        string = strftime('%H:%M:%S %p')
        self.clocklbl.config(text=string + " " + str(datetime.now().date()))
        self.clocklbl.after(1000, self.gettime)

    def mynotify(self):
        self.f=0
        flag=0
        while self.f==0:
            for match in self.matches:
                if (match['mchstate'] == 'inprogress'):
                    live = self.c.livescore(match['id'])
                    mymatch = match['team1']['name'] + ' Vs ' + match['team2']['name'] + "\n" + 'Batting ' + \
                              live['batting']['team'] + "\n" + \
                              live['batting']['score'][0]['runs'] + '/' + live['batting']['score'][0]['wickets'] + ' ' + \
                              live['batting']['score'][0]['overs'] + ' overs' + "\n" + \
                              live['batting']['batsman'][0]['name'] + ' ' + live['batting']['batsman'][0]['runs'] + '(' + \
                              live['batting']['batsman'][0]['balls'] + ')*'
                    if len(live['batting']['batsman']) > 1:
                        mymatch += " " + live['batting']['batsman'][1]['name'] + ' ' + live['batting']['batsman'][1][
                            'runs'] + '(' + live['batting']['batsman'][1]['balls'] + ')*'
                    self.n.show_toast("Live Cricket",mymatch, duration=10)
                    flag=1
                    break
            if flag==1:
                for i in range(1,100000000):
                    if self.f==1:
                        break
            else:
                break


    # packing widgets to window
    def packwidgets(self):
        self.row1.pack(fill="both")
        self.gettime()
        self.clocklbl.grid(row=0, column=2, padx="10")
        self.weatherimglbl.grid(row=0, column=0)
        self.lblweather.grid(row=0, column=1)
        self.myweather.grid(row=1, column=0, columnspan=2, pady="10")
        self.getcityweatherlbl.grid(row=2, column=0, columnspan=3, padx="20", sticky=N)
        self.cityvarentry.grid(row=3, column=0, columnspan=3, padx="20", pady="10", sticky=N)
        self.row7.pack(fill="both")
        self.newstext.grid(row=1, column=0, sticky=W, pady="10")
        self.newslbl.grid(row=0, column=0, pady="10", sticky=W)

# dictionary class
class Dictionary:

    def __init__(self,tabControl):

        # add tab
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Dictionary")

        # creating new frame
        self.row2 = Frame(self.tab2)
        self.data = json.load(open("data.json"))
        self.lbl1 = Label(self.tab2, text='Enter a word to search')

        # entry for accepting a word to search
        self.display = StringVar()
        self.dictentry = Entry(self.tab2, textvariable=self.display)

        # text Widget to display meanings of words
        self.meaning = Text(self.row2, bg="lightyellow")
        self.meaning.bind("<Double-Button-1>", self.copy_text_to_clipboard)

        #search button
        self.search = Button(self.tab2, text="SEARCH", command=self.Search)

        # label
        self.lbl2 = Label(self.tab2, text="* - Double click on meaning text box to copy text to clipboard")

    # set properties of widgets
    def set(self):
        self.lbl1.config(font=('times', 20, 'bold'), pady="10")
        self.dictentry.config(font=('times', 15), bd=10)
        self.meaning.tag_configure("center", justify='center')
        self.meaning.tag_add("center", 1.0, "end")
        self.search.config(width=20,bg="lightgreen", pady="10")
        self.lbl2.config(font=('courier', 8, 'bold'), bg="lightblue")

    # a dialog msg asking for confirmation
    def dialogmsg(self,w):
        if askyesno('Verify', w):
            return "Y"
        else:
            return "N"

    # copy text to clipboard on double click on text widget of dictionary
    def copy_text_to_clipboard(self,event):
        field_value = event.widget.get("1.0", 'end-1c')  # get field value from event, but remove line return at end
        root.clipboard_clear()  # clear clipboard contents
        root.clipboard_append(field_value)  # append new value to clipbaord

    # clear dictionary entry
    def clear_search(self):
        self.dictentry.delete(0, END)

    # get meaning of word
    def translate(self,w):
        # convert to lower case
        w = w.lower()
        # clear entry widget
        self.clear_search()
        # check for differnt cases
        if w in self.data:
            return self.data[w]
        elif w.title() in self.data:
            return self.data[w.title()]
        elif w.upper() in self.data:  # in case user enters words like USA or NATO
            return self.data[w.upper()]
        elif len(get_close_matches(w, self.data.keys())) > 0:
            ans = self.dialogmsg("Did you mean %s instead?" % get_close_matches(w, self.data.keys())[0])
            if ans == "Y":
                return self.data[get_close_matches(w, self.data.keys())[0]]
            elif ans == "N":
                return "The word doesn't exist. Please double check it."
            else:
                return "We didn't understand your entry."
        else:
            return "The word doesn't exist. Please double check it."
    # checking for errors or wrong info and add meaning to text widget
    def Search(self):
        if (self.display.get() != "" or self.display.get() != None):
            ss = self.display.get()
            i = 1
            output = self.translate(ss)
            if not ("The word doesn't exist" in output or "We didn't understand your entry." in output):
                self.meaning.insert(END, "MEANING -\n")
            if type(output) == list:
                for item in output:
                    # add meaning to text widget
                    self.meaning.insert(END, str(i) + ". " + item + "\n\n")
                    i += 1
            else:
                self.meaning.insert(END, output + "\n\n")
    # pack widgets on screen
    def packwidgets(self):
        self.lbl1.pack()
        self.dictentry.pack()
        self.row2.pack(fill=X,padx="10")
        self.meaning.pack(pady=10)
        self.search.pack()
        self.lbl2.pack(pady=10)

class TranslateText:
    def __init__(self,tabControl):
        # add tab
        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text="Translate")

        # label for prompting user to enter a sentence or a word to translate
        self.lbl3 = Label(self.tab3, text='Enter Something in English to Translate')

        # entry to accept user input
        self.mysentence = StringVar()
        self.sentence = Entry(self.tab3, textvariable=self.mysentence)

        # select language to translate into from the listbox
        self.lbl4 = Label(self.tab3, text='Select a language -')
        self.Lb = Listbox(self.tab3)
        self.languages = ['german', 'hindi', 'spanish', 'italian', 'chinese', 'japanese', 'french']

        # Label to display the translated text
        self.ttxt = StringVar()
        self.translatedtext = Label(self.tab3, bg="lightgreen", textvariable=self.ttxt, wraplength=500)

        # creating new Frame to add buttons in it
        self.row3 = Frame(self.tab3)
        # button to enable translation
        self.GO = Button(self.row3, text="GO", command=self.go)
        # button to clear all input and results from previous search
        self.CLEAR = Button(self.row3, text="CLEAR", command=self.clear_text)

    # set properties and perform basic operations on widgets
    def set(self):
        self.lbl3.config(font=('times', 20, 'bold'), pady="20")
        self.sentence.config(font=('times', 20), bd=10, width=40)
        self.lbl4.config(font=('times', 20, 'bold'), pady="20")
        k = 1
        for ll in self.languages:
            self.Lb.insert(k, ll)
            k += 1
        self.translatedtext.config(font=('times', 20, 'bold'), width=30)
        self.GO.config(width=10, height=2, bg="lightgreen")
        self.row3.columnconfigure(0, weight=1)
        self.row3.columnconfigure(1, weight=1)
        self.CLEAR.config(width=10, height=2, bg="lightblue")

    # clear data in widgets of translate tab
    def clear_text(self):
        self.sentence.delete(0, END)
        self.Lb.select_clear(ACTIVE)
        self.ttxt.set("")

    # method to translate a word or a sentence into selected language
    def go(self):
        # check if input is not empty
        if self.mysentence.get() != None and self.mysentence.get() != "":
            lang = str(self.Lb.get(ACTIVE))
            if lang != "" or lang != None:
                # translator module to translate the text
                translator = Translator(to_lang=lang)
                translation = translator.translate(self.mysentence.get())
                # set translated text to label
                self.ttxt.set(lang + " - " + translation + "\n")
                # pack label to screen
                self.translatedtext.pack(pady=10)
            else:
                # no language selected from the list
                self.ttxt.set("please select a valid language from the list\n")

        else:
            # invalid input
            showwarning("invalid input", "Enter a valid sentence")

    # pack widgets to screen
    def packwidgets(self):
        self.lbl3.pack()
        self.sentence.pack()
        self.lbl4.pack()
        self.Lb.pack()
        self.row3.pack(fill=X)
        self.GO.grid(row=0, column=0, padx=10, pady=20, sticky=E)
        self.CLEAR.grid(row=0, column=1, pady=20, sticky=W)

#Bookstore class
class BookStore:
    def __init__(self,tabControl):
        # add tab
        self.tab4 = ttk.Frame(tabControl)
        tabControl.add(self.tab4, text="BookStore")
        # creating new frame to add widgets
        self.row4 = Frame(self.tab4)
        # label for book info
        self.l1 = Label(self.row4, text="Title")
        self.l2 = Label(self.row4, text="Author")
        self.l3 = Label(self.row4, text="Year")
        self.l4 = Label(self.row4, text="ISBN")

        # entries for accepting bookinfo as input
        self.title_text = StringVar()
        self.e1 = Entry(self.row4, textvariable=self.title_text)
        self.author_text = StringVar()
        self.e2 = Entry(self.row4, textvariable=self.author_text)
        self.year_text = StringVar()
        self.e3 = Entry(self.row4, textvariable=self.year_text)
        self.isbn_text = StringVar()
        self.e4 = Entry(self.row4, textvariable=self.isbn_text)

        #listbox to show entries in the database
        self.list1 = Listbox(self.row4, height=10, width=40)
        # adding scrollbar to listbox
        self.sb1 = Scrollbar(self.row4)
        # buttons for differnt operations
        self.b1 = Button(self.row4, text="View all", width=12,bg="lightgreen", command=self.view_command)
        self.b2 = Button(self.row4, text="Search entry", width=12,bg="lightblue", command=self.search_command)
        self.b3 = Button(self.row4, text="Add entry", width=12,bg="lightgreen", command=self.add_command)
        self.b4 = Button(self.row4, text="Update selected", width=12,bg="lightblue", command=self.update_command)
        self.b5 = Button(self.row4, text="Delete selected", width=12,bg="lightgreen", command=self.delete_command)

        # creating another frame for add online book search functionality
        self.row5 = Frame(self.tab4)
        self.searchbooklbl = Label(self.row5, text="Search a book online :", font=('times', 15, 'bold'))
        self.bookentrytext = StringVar()
        self.searchbookentry = Entry(self.row5, textvariable=self.bookentrytext, bd=5, font=('times', 15))

        # frame for adding search results label
        self.row6 = Frame(self.tab4)
        self.volumeinfo = Label(self.row6, font=('times', 15), justify="left", bg="lightblue")
        self.searchbookentry.bind("<Return>", self.bookinfo)

    # get bookinfo from google api
    def bookinfo(self,event):
        # get bookname entered by user
        ss = self.bookentrytext.get()
        try:
            if ss != "":
                ss = ss.replace(" ", "")
                # calling searchbook method from bbcnews.py
                book = searchbooks(ss)
                # get required info from dictionary object book
                book_title = book["volumeInfo"]["title"]
                book_authors = book["volumeInfo"]["authors"]
                # if pagcount is present in bookinfo
                if "pageCount" in book["volumeInfo"].keys():
                    pagecount = str(book["volumeInfo"]["pageCount"])
                else:
                    pagecount = "unknown"

                book_lang = book["volumeInfo"]["language"]
                published_date = book["volumeInfo"]["publishedDate"]
                isbn = book["volumeInfo"]["industryIdentifiers"][1]["identifier"]
                summary = textwrap.fill(book["searchInfo"]["textSnippet"], width=65)
                # display bookinfo in label
                self.volumeinfo.config(text="\nTitle: " + book_title + "\nAuthor(s): " + ",".join(
                    book_authors) + "\nPublished-Date: " + published_date + "\nISBN: " + isbn
                                       + "\nPage count: " + pagecount + "\nLanguage: " + book_lang + "\nSummary:\n" + summary)
                self.volumeinfo.grid(row=1, sticky=W)
                #clear book entry
                self.bookentrytext.set("")
            else:
                # book not found
                showerror("message", "please enter a valid book")
        except:
            # book not found
            showerror("message", "book not found ,maybe try providing author name or isbn")

    # get the selected item from the listbox
    def get_selected_row(self,event):
        try:
            global selected_tuple
            index = self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            # automatically put the details in the entries of frame row4
            self.e1.delete(0, END)
            # set title
            self.e1.insert(END, selected_tuple[1])
            self.e2.delete(0, END)
            # set author
            self.e2.insert(END, selected_tuple[2])
            self.e3.delete(0, END)
            # set year
            self.e3.insert(END, selected_tuple[3])
            self.e4.delete(0, END)
            # set isbn
            self.e4.insert(END, selected_tuple[4])
        except IndexError:
            pass

    # view contents of bookstore database
    def view_command(self):
        self.list1.delete(0, END)
        for row in backend.view():
            self.list1.insert(END, row)

    # search for a book in database
    def search_command(self):
        self.list1.delete(0, END)
        for row in backend.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.list1.insert(END, row)

    # add a book into database
    def add_command(self):
        if self.title_text.get()!="" and self.author_text.get()!="" and self.year_text.get()!="" and self.isbn_text.get()!="":
            backend.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
            self.list1.delete(0, END)
            self.list1.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))
        else:
            showerror("Error","please provide all the required info of book")
    # delete entry from database
    def delete_command(self):
        try:
            backend.delete(selected_tuple[0])
        except:
            showerror("Error","no item to delete or select an item first")
    # update details of a book
    def update_command(self):
        try:
            backend.update(selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        except:
            showerror("Error","Nothing to update")
    # pack widgets on screen
    def packwidgets(self):
        self.row4.pack(side="top")
        self.l1.grid(row=0, column=0, padx="20", pady="10")
        self.l2.grid(row=0, column=2, padx="20", pady="10")
        self.l3.grid(row=1, column=0, padx="20", pady="10")
        self.l4.grid(row=1, column=2, padx="20", pady="10")

        self.e1.grid(row=0, column=1, padx="20", pady="10")
        self.e2.grid(row=0, column=3, padx="20", pady="10")
        self.e3.grid(row=1, column=1, padx="20", pady="10")
        self.e4.grid(row=1, column=3, padx="20", pady="10")
        self.list1.grid(row=2, column=0, rowspan=10, columnspan=2, padx="20")
        self.sb1.grid(row=2, column=2, rowspan=10)
        self.list1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.list1.yview)
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        self.b1.grid(row=2, column=3, pady="5")
        self.b2.grid(row=3, column=3, pady="5")
        self.b3.grid(row=4, column=3, pady="5")
        self.b4.grid(row=5, column=3, pady="5")
        self.b5.grid(row=6, column=3, pady="5")

        self.row5.pack(pady="20")
        self.searchbooklbl.grid(row=0, column=0, sticky=N, padx="10")
        self.searchbookentry.grid(row=0, column=1, sticky=N)

        self.row6.pack()

# voice assistant class
class VoiceAssistant:

    def __init__(self,tabControl):
        # add tab
        self.tab5 = ttk.Frame(tabControl)
        tabControl.add(self.tab5, text="Voice Assistant")

        # creating a new Frame to add widgets
        self.row7 = Frame(self.tab5)

        self.label1 = ttk.Label(self.row7, text='Query:')
        # get search query from user as input
        self.entry1 = ttk.Entry(self.row7, width=40)
        self.radiobtn = StringVar()
        self.entry1.bind('<Return>', self.get)
        self.photo = PhotoImage(file='images/microphone.png').subsample(30,30)

        #Mic button
        self.MyButton6 = Button(self.row7, image=self.photo, command=self.listenvoice, bd=0, activebackground='#c1bfbf',
                           overrelief='groove', relief='sunken')

        # search button
        self.MyButton1 = ttk.Button(self.row7, text='Search', width=10, command=self.callback)

        # add radio buttons in new frame
        self.row8 = Frame(self.tab5)

        # radio buttons
        self.MyButton2 = ttk.Radiobutton(self.row8, text='Google', value='google', variable=self.radiobtn)
        self.MyButton3 = ttk.Radiobutton(self.row8, text='Duck', value='duck', variable=self.radiobtn)
        self.MyButton4 = ttk.Radiobutton(self.row8, text='Amazon-Books', value='amz', variable=self.radiobtn)
        self.MyButton5 = ttk.Radiobutton(self.row8, text='Youtube', value='ytb', variable=self.radiobtn)

        # frame to display info returned
        self.row9 = Frame(self.tab5)
        self.mylabel = Label(self.row9, text="* say jarvis before asking a question through voice", bg="lightblue",
                        font=('courier', 10, 'bold'), wraplength=500)
        self.jarvistext = Text(self.row9, font=('courier', 15, 'bold'), bg="lightyellow")

        # set focus on entry widget
        self.entry1.focus()
        # set google radiobutton selected by default
        self.radiobtn.set('google')

    # method to greet me on tab click
    def wishMe(self):
        hour = int(datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning sir!")

        elif hour >= 12 and hour < 18:
            speak("Good Afternoon sir!")

        else:
            speak("Good Evening sir!")

    # callback method for search query provided in assistant tab and search for the query on selected search engine
    def callback(self):
        if self.radiobtn.get() == 'google' and self.entry1.get() != '':
            webbrowser.open('http://google.com/search?q=' + self.entry1.get())

        elif self.radiobtn.get() == 'duck' and self.entry1.get() != '':
            webbrowser.open('http://duckduckgo.com/?q=' + self.entry1.get())

        elif self.radiobtn.get() == 'amz' and self.entry1.get() != '':
            webbrowser.open('https://amazon.com/s/?url=search-alias%3Dstripbooks&field-keywords=' + self.entry1.get())

        elif self.radiobtn.get() == 'ytb' and self.entry1.get() != '':
            webbrowser.open('https://www.youtube.com/results?search_query=' + self.entry1.get())

        else:
            pass

    # bind method for search entry which works the same as callback ,triggered when user presses <enter> key
    def get(self,event):
        if self.radiobtn.get() == 'google' and self.entry1.get() != '':
            webbrowser.open('http://google.com/search?q=' + self.entry1.get())

        elif self.radiobtn.get() == 'duck' and self.entry1.get() != '':
            webbrowser.open('http://duckduckgo.com/?q=' + self.entry1.get())

        elif self.radiobtn.get() == 'amz' and self.entry1.get() != '':
            webbrowser.open('https://amazon.com/s/?url=search-alias%3Dstripbooks&field-keywords=' + self.entry1.get())

        elif self.radiobtn.get() == 'ytb' and self.entry1.get() != '':
            webbrowser.open('https://www.youtube.com/results?search_query=' + self.entry1.get())

        else:
            speak("please select a search engine sir")

    # method for speech_recognition and provide appropriate results
    def listenvoice(self):
        self.MyButton6.config(state=DISABLED)
        try:
            mixer.music.load('chime1.mp3')
            mixer.music.play()
            t=threading.Thread(target=self.performinthread)
            t.daemon=True
            t.start()
        except:
            self.MyButton6.config(state=NORMAL)
    def performinthread(self):
        query = myCommand()
        if query != "" and query != None:
            query = query.lower()
            self.entry1.focus()
            self.entry1.delete(0, END)
            self.entry1.insert(0, query)
            # open content on web browser based on speech recognition
            if 'open youtube' in query:
                speak('okay sir')
                webbrowser.open('www.youtube.com')

            elif 'bye' in query or 'go to sleep' in query or 'shut up' in query:
                speak('Goodbye sir , have a nice day')

            elif 'open google' in query:
                speak('okay')
                webbrowser.open('www.google.co.in')

            elif 'open gmail' in query:
                speak('okay')
                webbrowser.open('www.gmail.com')

            elif "what\'s up" in query or 'how are you' in query:
                stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
                speak(random.choice(stMsgs))
            elif "jarvis" in query:
                query = query[7:]
                try:
                    try:
                        res = client.query(query)
                        results = next(res.results).text
                        self.jarvistext.insert(END, results + "\n")
                        speak('Got it.')
                        speak(results)


                    except:
                        # search on wikipedia
                        results = wikipedia.summary(query, sentences=2)
                        self.jarvistext.insert(END, results + "\n")
                        speak('Got it.')
                        speak('WIKIPEDIA says - ')
                        speak(results)

                except:
                    speak('may be you should google it sir')
                    webbrowser.open('www.google.com')

            # get the selected radiobutton
            elif self.radiobtn.get() == 'google':
                webbrowser.open('http://google.com/search?q=' + query)

            elif self.radiobtn.get() == 'duck':
                webbrowser.open('http://duckduckgo.com/?q=' + query)

            elif self.radiobtn.get() == 'amz':
                webbrowser.open('https://amazon.com/s/?url=search-alias%3Dstripbooks&field-keywords=' + query)

            elif self.radiobtn.get() == 'ytb':
                webbrowser.open('https://www.youtube.com/results?search_query=' + query)
            else:
                speak("pardon me sir!")
        self.MyButton6.config(state=NORMAL)

    # pack widgets on screen
    def packwidgets(self):
        self.label1.grid(row=0, column=0, sticky='W', padx="10")
        self.entry1.grid(row=0, column=1, padx="10", columnspan=4)
        self.MyButton6.grid(row=0, column=5)
        self.MyButton1.grid(row=0, column=6, padx="10")
        self.row7.pack(fill="x", pady="20")
        self.row8.pack(fill="x")
        self.MyButton2.grid(row=0, column=0, sticky=N, padx="10")
        self.MyButton3.grid(row=0, column=1, sticky=N, padx="10")
        self.MyButton4.grid(row=0, column=2, padx="10")
        self.MyButton5.grid(row=0, column=3, sticky=N, padx="10")
        self.row9.pack(pady="10")
        self.mylabel.pack()
        self.jarvistext.pack(expand="no", padx="10")

class MusicPlayer:

    def __init__(self,tabControl):
        # add tab
        self.tab6 = ttk.Frame(tabControl)
        tabControl.add(self.tab6, text="Music")
        self.statusbar = ttk.Label(self.tab6, text="Welcome to R.A.STUDIOS", relief=SUNKEN, anchor=W, font='Times 10 italic')

        self.playlist = []
        # playlist frame
        self.leftframe = Frame(self.tab6)
        self.playlistlbl = Label(self.leftframe, text="PlayList", font=('courier', 10, 'bold'), fg="red")
        self.playlistbox = Listbox(self.leftframe)

        # variable to store absolute location of file
        self.filename_path = None
        # playlist - contains the full path + filename
        # playlistbox - contains just the filename
        # Fullpath + filename is required to play the music inside play_music load function

        self.addBtn = ttk.Button(self.leftframe, text="+ Add", command=self.browse_file)
        self.delBtn = ttk.Button(self.leftframe, text="- Del", command=self.del_song)

        # rightframe containing music buttons
        self.rightframe = Frame(self.tab6)

        # 3 frames in rightframe
        self.topframe = Frame(self.rightframe)
        self.lengthlabel = ttk.Label(self.topframe, text='Total Length : --:--')
        self.currenttimelabel = ttk.Label(self.topframe, text='Current Time : --:--', relief=GROOVE)

        # variable to check if music is paused or muted
        self.paused = FALSE
        self.muted = FALSE

        self.middleframe = Frame(self.rightframe)
        # play button and photo on it
        self.playPhoto = PhotoImage(file='images/play.png')
        self.playBtn = ttk.Button(self.middleframe, image=self.playPhoto, command=self.play_music)

        # stop button and its photo
        self.stopPhoto = PhotoImage(file='images/stop.png')
        self.stopBtn = ttk.Button(self.middleframe, image=self.stopPhoto, command=self.stop_music)

        # pause button and its photo
        self.pausePhoto = PhotoImage(file='images/pause.png')
        self.pauseBtn = ttk.Button(self.middleframe, image=self.pausePhoto, command=self.pause_music)

        # Bottom Frame for volume, rewind, mute etc.
        self.bottomframe = Frame(self.rightframe)

        # rewind button and its photo
        self.rewindPhoto = PhotoImage(file='images/rewind.png')
        self.rewindBtn = ttk.Button(self.bottomframe, image=self.rewindPhoto, command=self.rewind_music)

        # mute button and its photo
        self.mutePhoto = PhotoImage(file='images/mute.png')
        self.volumePhoto = PhotoImage(file='images/volume.png')
        self.volumeBtn = ttk.Button(self.bottomframe, image=self.volumePhoto, command=self.mute_music)

        # scale to set volume of song
        self.scale = ttk.Scale(self.bottomframe, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)

    # set properties of widgets
    def set(self):
        # read user's saved playlist
        with open('myplaylist.txt', 'r') as pl:
            for filename in pl.readlines():
                self.filename_path = filename[:-1]
                self.add_to_playlist(filename[:-1])
        pl.close()
        self.scale.set(70)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.7)

    # pack widgets to screen
    def packwidgets(self):
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.leftframe.pack(side=LEFT, padx=20)
        self.playlistlbl.pack(side=TOP)
        self.playlistbox.pack()
        self.addBtn.pack(side=LEFT)
        self.delBtn.pack(side=LEFT)

        self.rightframe.pack(side=RIGHT, padx=10, pady=20)

        self.topframe.pack()
        self.lengthlabel.pack(pady=5)
        self.currenttimelabel.pack()

        self.middleframe.pack(pady=30, padx=20)
        self.playBtn.grid(row=0, column=0, padx=5)
        self.stopBtn.grid(row=0, column=1, padx=5)
        self.pauseBtn.grid(row=0, column=2, padx=5)
        self.bottomframe.pack()
        self.rewindBtn.grid(row=0, column=0)
        self.volumeBtn.grid(row=0, column=1)
        self.scale.grid(row=0, column=2, pady=15, padx=30)

    # browse file to add to playlist
    def browse_file(self):
        self.filename_path = askopenfilename()
        self.add_to_playlist(self.filename_path)
        # add file to playlist
        with open('myplaylist.txt', 'a') as pl:
            pl.write(self.filename_path + '\n')
        pl.close()
        mixer.music.queue(self.filename_path)

    # add song to playlist llistbox
    def add_to_playlist(self,filename):
        filename = os.path.basename(filename)
        index = 0
        self.playlistbox.insert(index, filename)
        self.playlist.insert(index, self.filename_path)
        index += 1

    # delete selected song from playlist
    def del_song(self):
        selected_song = self.playlistbox.curselection()
        if len(selected_song) != 0:
            selected_song = int(selected_song[0])
            self.playlistbox.delete(selected_song)
            self.playlist.pop(selected_song)
        else:
            showerror("error", "no song selected")

    # show info about song
    def show_details(self,play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lengthlabel['text'] = "Total Length" + ' - ' + timeformat

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    # start counting length of song
    def start_count(self,t):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and mixer.music.get_busy():
            if self.paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                sleep(1)
                current_time += 1

    # play music
    def play_music(self):

        if self.paused:
            mixer.music.unpause()
            self.statusbar['text'] = "Music Resumed"
            self.paused = FALSE
        else:
            try:
                self.stop_music()
                sleep(1)
                selected_song = self.playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_it =self. playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                self.statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
                self.show_details(play_it)
            except Exception as e:
                print(e)
                showerror('File not found', 'could not find the file. Please check again.')

    # stop music
    def stop_music(self):
        mixer.music.stop()
        self.statusbar['text'] = "Music Stopped"

    # pause music
    def pause_music(self):
        self.paused = TRUE
        mixer.music.pause()
        self.statusbar['text'] = "Music Paused"

    # rewind music
    def rewind_music(self):
        self.play_music()
        self.statusbar['text'] = "Music Rewinded"

    # set volume of music
    def set_vol(self,val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

    # mute music
    def mute_music(self):
        if self.muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            self.volumeBtn.configure(image=self.volumePhoto)
            self.scale.set(70)
            self.muted = FALSE
        else:  # mute the music
            mixer.music.set_volume(0)
            self.volumeBtn.configure(image=self.mutePhoto)
            self.scale.set(0)
            self.muted = TRUE

# class to perform operations of images
class ImageAnalyze:
    def __init__(self,tabControl):
        # add tab
        self.tab7 = ttk.Frame(tabControl)
        tabControl.add(self.tab7, text="Images")
        # panelA for loading image and PanelB for showing result image
        self.panelA = None
        self.panelB = None
        # cv2 image
        self.image = None
        # absolute path of image
        self.path = None
        # saveimage type
        self.saveimg = None
        # image name and location
        self.imgname = None
        # response object to download images from web
        self.response = google_images_download.googleimagesdownload()
        # frame containing buttons to perform operations on images
        self.row10 = Frame(self.tab7)
        self.btn = Button(self.row10, text="Select an image", command=lambda m="Select an image": self.image_perform(m))
        self.btn1 = Button(self.row10, text="Blur image", command=lambda m="Blur image": self.image_perform(m))
        self.btn2 = Button(self.row10, text="Detect Edges", command=lambda m="Detect Edges": self.image_perform(m))
        self.btn3 = Button(self.row10, text="Save image to desktop", command=lambda m="Save image to desktop": self.image_perform(m))
        self.btn4 = Button(self.row10, text="Transposed image", command=lambda m="Transposed image": self.image_perform(m))
        self.btn5 = Button(self.row10, text="Resize image", command=lambda m="Resize image": self.image_perform(m))
        self.btn6 = Button(self.row10, text="Create Thumbnail", command=lambda m="Create Thumbnail": self.image_perform(m))
        self.btn7=Button(self.row10, text="Extract Text", command=lambda m="Extract Text": self.image_perform(m))

        # set width and height of image for resizing and creating thumbnail
        self.row11 = Frame(self.tab7)
        self.lblw = Label(self.row11, text='width')

        self.lblh = Label(self.row11, text='height')

        self.widthvar = StringVar()
        self.widthent = Entry(self.row11, textvariable=self.widthvar, width=8)

        self.heighthvar = StringVar()
        self.heightent = Entry(self.row11, textvariable=self.heighthvar, width=8)

        # frame containing image download entry to accept search query to download related images
        self.row12 = Frame(self.tab7)
        self.lbldownload = Label(self.row12, text='Search for images to download')

        self.downloadimg = StringVar()
        self.imgentry = Entry(self.row12, textvariable=self.downloadimg)

        # bind method to download image on pressing <Enter>
        self.imgentry.bind("<Return>",self.downloadimages)

        # image to text
        self.imgtotxtvar=StringVar()
        self.imgtotxtent=Entry(self.row12,textvariable=self.imgtotxtvar)
        self.largeimg=None
        self.flag=0
        self.newwin=None


    # show full size image on label click
    def showlargeimg(self,event):

        if self.largeimg!=None and self.flag==0:
            self.newwin = Toplevel(root)
            self.newwin.geometry(str(self.wd)+"x"+str(self.ht)+"+100+5")
            self.flag=1

            self.newwin.protocol("WM_DELETE_WINDOW", self.winclose)
            canv = Canvas(self.newwin, relief=SUNKEN)

            sbarV = Scrollbar(self.newwin, orient=VERTICAL)
            sbarH = Scrollbar(self.newwin, orient=HORIZONTAL)

            sbarV.config(command=canv.yview)
            sbarH.config(command=canv.xview)

            canv.config(width=400, height=200)
            # canv.config(scrollregion=(0,0,1000, 1000))
            # canv.configure(scrollregion=canv.bbox('all'))
            canv.config(highlightthickness=0)
            canv.config(yscrollcommand=sbarV.set)
            canv.config(xscrollcommand=sbarH.set)

            sbarV.pack(side=RIGHT, fill=Y)
            sbarH.pack(side=BOTTOM, fill=X)

            canv.pack(side=LEFT, expand=YES, fill=BOTH)
            width, height = self.wd,self.ht
            canv.config(scrollregion=(0, 0, width, height))
            self.imgtag = canv.create_image(0, 0, anchor="nw", image=self.largeimg)


    def winclose(self):
        self.flag = 0
        self.newwin.destroy()

        # set properties of widgets
    def set(self):
        self.lblw.config(font=('times', 15, 'bold'))
        self.lblh.config(font=('times', 15, 'bold'))
        self.widthent.config(bd=5)
        self.row11.columnconfigure(0, weight=1)
        self.row11.columnconfigure(1, weight=1)
        self.heightent.config(bd=5)
        self.lbldownload.config(font=('times', 11, 'bold'))
        self.imgentry.config(font=('times', 12), bd=10, width=30)
        self.imgtotxtvar.set("Text from image if any")
        self.imgtotxtent.config(font=('times', 11), width=50)

    # pack widgets on screen
    def packwidgets(self):
        self.row11.pack()
        self.lblw.grid(row=0, column=0, sticky="w", padx="10")
        self.lblh.grid(row=0, column=1, sticky="e", padx="10")
        self.widthent.grid(row=1, column=0, sticky="w", padx="10", pady="5")
        self.heightent.grid(row=1, column=1, sticky="e", padx="10", pady="5")
        self.row10.pack(side="bottom", fill="x")
        self.btn3.grid(row=1, column=0, pady="10", padx="30")
        self.btn4.grid(row=1, column=1, pady="10", padx="30")
        self.btn2.grid(row=1, column=2, pady="10", padx="30")
        self.btn1.grid(row=2, column=0, pady="10", padx="30")
        self.btn.grid(row=2, column=1, pady="10", padx="30")
        self.btn5.grid(row=2, column=2, pady="10", padx="30")
        self.btn6.grid(row=3, column=0, pady="10", padx="30")
        self.btn7.grid(row=3, column=1, pady="10", padx="30")

        self.row12.pack(side="bottom", fill="x")
        self.lbldownload.grid(row=0, column=0, padx="10")
        self.imgentry.grid(row=0, column=1, padx="5")
        self.imgtotxtent.grid(row=1,columnspan=3,padx="10")

    # method for downloading images from web
    def downloadimages(self,event):
        if self.downloadimg.get() == "":
            showerror("error", "please provide a search query in input")
        else:
            arguments = {"keywords": self.downloadimg.get(),
                         "format": "jpg",
                         "limit": 4,
                         "print_urls": True,
                         "size": "medium",
                         "aspect_ratio": "panoramic",
                         "output_directory": r"C:\Users\hp\Desktop\mynewimages",
                         "safe_search": True,
                         "help": True
                         }
            try:
                self.response.download(arguments)
                self.downloadimg.set("")

                # Handling File NotFound Error
            except FileNotFoundError:

                arguments = {"keywords": self.downloadimg.get(),
                             "format": "jpg",
                             "limit": 1,
                             "print_urls": True,
                             "size": "medium"}

                # Providing arguments for the searched query
                try:
                    # Downloading the photos based
                    # on the given arguments
                    self.response.download(arguments)
                except:
                    pass

    # set image properties
    def set_img_prop(self,imagename, svimg, method):
        self.resultimg(svimg, method)
        self.imgname = imagename
        self.saveimg = svimg

    # get result image converted into tkimage and displayed in panelB
    def resultimg(self,img, method="Y"):
        avgi = img
        if method == "Y":
            avgi = Image.fromarray(img)
        avgi = ImageTk.PhotoImage(avgi)
        if self.panelB is None:
            self.panelB = Label(self.tab7, image=avgi,width=200,height=250)
            self.panelB.image = avgi
            self.panelB.pack(side="right", padx=10)
        else:
            # update the pannels
            self.panelB.configure(image=avgi)
            self.panelB.image = avgi

    # method for performing various image manipulation operations
    def image_perform(self,method):
        if method == "Select an image":
            self.path = askopenfilename()
            if self.panelB != None:
                self.panelB.config(image="")
            if self.panelA != None:
                self.panelA.config(image="")
            if self.newwin!=None:
                self.flag=0
                self.newwin.destroy()
            try:
                if len(self.path) > 0:
                    # load the image from disk
                    self.image = cv2.imread(self.path)

                    # OpenCV represents images in BGR order; however PIL represents
                    # images in RGB order, so we need to swap the channels
                    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

                    # convert the images to PIL format...
                    self.image = Image.fromarray(self.image)
                    self.largeimg=self.image
                    self.wd,self.ht=self.image.size
                    self.largeimg = ImageTk.PhotoImage(self.largeimg)
                    # ...and then to ImageTk format
                    self.image = ImageTk.PhotoImage(self.image)
                    if self.panelA is None:
                        # the first panel will store our original image
                        self.panelA = Label(self.tab7, image=self.image,width=200,height=250)
                        self.panelA.image = self.image
                        self.panelA.bind('<Button-1>', self.showlargeimg)
                        self.panelA.pack(side="left", padx=10)

                    else:
                        # update the pannels
                        self.panelA.configure(image=self.image)
                        self.panelA.image = self.image

            except:
                showwarning("invalid image format", "please select a valid image")
        else:
            if self.panelA != None and len(self.path) > 0:
                self.image = cv2.imread(self.path)
                # convert from bgr to rgb
                avging = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

                if method == "Blur image":
                    avging = cv2.blur(avging, (10, 10))
                    self.set_img_prop("blur_img", avging, "Y")
                    self.saveimg = Image.fromarray(avging)

                elif method == "Detect Edges":
                    gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                    # convert to gray scale image
                    edged = cv2.Canny(gray, 50, 100)
                    self.set_img_prop("detect_edges_img", edged, "Y")
                    self.saveimg = Image.fromarray(edged)

                elif method == "Transposed image":
                    # convert cv2  to PIL image object
                    transposed_img = Image.fromarray(avging)
                    transposed_img = transposed_img.transpose(Image.FLIP_LEFT_RIGHT)
                    self.set_img_prop("transposed_img", transposed_img, "N")

                elif method == "Save image to desktop":
                    if self.saveimg != None:
                        print("yes")
                        self.saveimg.save("C:\\Users\hp\Desktop\\" + self.imgname + ".jpg")
                        showinfo("message", "image saved succesfully")
                    else:
                        showerror("error", "no changes made to original image")

                elif method == "Resize image":
                    if self.heighthvar.get() == "" or self.widthvar.get() == "":
                        showinfo("message", "Please specify height and width in pixels")
                    else:
                        width, height = int(self.widthvar.get()), int(self.heighthvar.get())
                        resize_img = Image.fromarray(avging)
                        resize_img = resize_img.resize((width, height))
                        self.set_img_prop("resized_image" + self.widthvar.get() + "x" + self.heighthvar.get(), resize_img, "N")

                elif method == "Create Thumbnail":
                    if self.heighthvar.get() == "" or self.widthvar.get() == "":
                        showinfo("message", "Please specify height and width in pixels")
                    else:
                        width, height = int(self.widthvar.get()), int(self.heighthvar.get())
                        thumbnail_img = Image.fromarray(avging)
                        thumbnail_img.thumbnail((width, height))
                        self.imgname = "thumbnail_image" + self.widthvar.get() + "x" + self.heighthvar.get()
                        self.saveimg = thumbnail_img
                        showinfo("message", "Thumbnail created successfully")


                elif method == "Extract Text":
                    # convert the image to PIL image and further convert it to gray scale image
                    txtimg=Image.fromarray(avging).convert('L')
                    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
                    imgtext = pytesseract.image_to_string(txtimg)
                    self.imgtotxtvar.set(imgtext)


            else:
                showwarning("invalid image format", "please select a valid image")


#create root window variable
root=Tk()
# object for root window
windw=Window(root)
# object for homepage tab
home=Homepage(windw.tabControl)
home.set()
home.packwidgets()

#object for dictionary tab
dictionary=Dictionary(windw.tabControl)
dictionary.set()
dictionary.packwidgets()

# object for tranlsate tab
translatetext=TranslateText(windw.tabControl)
translatetext.set()
translatetext.packwidgets()

# object fron bookstore tab
bookstore=BookStore(windw.tabControl)
bookstore.packwidgets()

# object for voice assistant tab
mixer.init()
voiceassistant=VoiceAssistant(windw.tabControl)
voiceassistant.packwidgets()

# object for music player
musicplayer=MusicPlayer(windw.tabControl)
musicplayer.set()
musicplayer.packwidgets()

def on_closing():
    musicplayer.stop_music()
    home.f=1
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# object for imageanalyze
imageanalyze=ImageAnalyze(windw.tabControl)
imageanalyze.set()
imageanalyze.packwidgets()
# set window on top
root.wm_attributes('-topmost', 1)
#run root window
root.mainloop()