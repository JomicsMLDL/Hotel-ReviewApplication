
import pandas as pd
import requests

from bs4 import BeautifulSoup
from textblob import TextBlob

"""Specify The URL and CSV filename."""

URL = 'https://www.tripadvisor.in/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html'
csvfilename='Review.csv'

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

reviews_list=[]
for quote in soup.find_all("div", {"class": "quote isNew"}):
        fulllink = 'https://www.tripadvisor.in' + quote.find("a")['href'] 
        rq=requests.get(fulllink)
        rsoup = BeautifulSoup(rq.content, 'html5lib')
        "Scrap Review"
        review = rsoup.find("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})
        review_text = review.find("p",{"class": "partial_entry"}).text
        rating = rsoup.find("div", {"class": "altHeadInline"})
        "if review is negative or positive"
        pos=TextBlob(review_text)
        sentiment=pos.sentiment.polarity
        if sentiment>0:
            score=1 #positive
        else:
            score=0#negative
        ratings=rating.next.next.next.next["class"][1][7:]
        reviews_list.append([review_text,ratings,score])


""" Number Of Reviews"""

pages=str(soup.find_all("div",{"class" : "pagination-details"}))
NoOfPage=(pages.split('</b>')[2]).split('<b>')[1]

if ',' in NoOfPage:
    Nreview=""
    splitpage=NoOfPage.split(',')
    for i in splitpage:
        Nreview=Nreview+i
Nreview=int(Nreview)
NoPage=Nreview/5

"""Find SubURLS."""
urlsplit=URL.split('Reviews')
SubURL=[]
for k in range(5,Nreview,5):
    sub=urlsplit[0] + 'Reviews-or'+str(k)+urlsplit[1]
    SubURL.append(sub)
needsuburl=SubURL[0:100]
"""Scrap review from every SUBURL"""
for sub in needsuburl:
    r = requests.get(sub)
#    time.sleep(2)
    soup = BeautifulSoup(r.content, 'html5lib')

    for quote in soup.find_all("div", {"class": "quote"}):
            fulllink = 'https://www.tripadvisor.in' + quote.find("a")['href'] 
            rq=requests.get(fulllink)
            rsoup = BeautifulSoup(rq.content, 'html5lib')
            "Scrap Review"
            review = rsoup.find("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})
            review_text = review.find("p",{"class": "partial_entry"}).text
            rating = rsoup.find("div", {"class": "altHeadInline"})
            "if review is negative or positive"
            pos=TextBlob(review_text)
            sentiment=pos.sentiment.polarity
            if sentiment>0:
                score=1 #positive
            else:
                score=0#negative
            ratings=rating.next.next.next.next["class"][1][7:]
            reviews_list.append([review_text,ratings,score])





"""Write in a csv file"""
df = pd.DataFrame(reviews_list)
df.to_csv(csvfilename,header=['Review','Rating','Score'])


