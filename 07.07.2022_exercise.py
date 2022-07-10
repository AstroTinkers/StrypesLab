import urllib.request
from tkinter import *
from urllib import *
import feedparser
feed = feedparser.parse("http://rss.slashdot.org/Slashdot/slashdot.rss")


def scrape_data(news_dict):
    feed = feedparser.parse("http://rss.slashdot.org/Slashdot/slashdot.rss")
    for entry in range(len(feed["entries"])):
        title = str(feed["entries"][entry]["title"])
        article = str(feed["entries"][entry]["summary"])
        article = article[:article.index("<p>")]
        news_dict[title] = article


def populate_title_listbox(news_dict):
    n = 1
    for title in news_dict:
        headlines.insert(n, title)
        n += 1


def article_reader(evt):
    global news_collector
    article = headlines.get(headlines.curselection())
    news.config(text=news_collector[article])


news_collector = dict()

main_window = Tk()
main_window.title("Rss Feed")
main_window.geometry("680x1000")
main_window.resizable(False, False)
main_window.config(bg='light grey')
frame = Frame(main_window, bg='light grey')
frame.grid()

headlines = Listbox(frame, selectmode=SINGLE, font=("Times New", 11), height=20, width=85, justify=CENTER,
                    bg='dark grey', fg='black')
headlines.grid(row=0, sticky="new")
headlines.bind("<<ListboxSelect>>", article_reader)
news = Label(frame, text="", justify=CENTER, wraplength=500, bg='light grey', fg='black')
news.grid(row=1, sticky="new")


scrape_data(news_collector)
populate_title_listbox(news_collector)
main_window.mainloop()
