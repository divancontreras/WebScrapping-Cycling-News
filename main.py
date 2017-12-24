import requests
from bs4 import BeautifulSoup
import pyrebase
from googletrans import Translator
import json
config_settings = {
    "apiKey": "312169273725",
    "authDomain": "arodarmty.firebaseio.com",
    "databaseURL": "https://arodarmty.firebaseio.com",
    "storageBucket": "arodarmty.appspot.com",
    "serviceAccount": "serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config_settings)
db = firebase.database()

translator = Translator()
raw_page = requests.get("http://www.cyclingnews.com/news/")
data = raw_page.text
soup = BeautifulSoup(data, "html.parser")
news_articles = soup.find_all("article")
for article in news_articles:
    inside_page = requests.get("http://www.cyclingnews.com"+article.find("a")['href']).text
    soup_inside = BeautifulSoup(inside_page, "html.parser")
    inside_body = soup_inside.find("div", class_="post-page")
    paragraphs = inside_body.find_all("p")
    images = soup_inside.find_all("figure", class_="gallery-item")
    text_body = []
    gallery_body = []
    body_es = []
    for paragraph in paragraphs:
        text_body.append(paragraph.text)
        body_es.append(str(translator.translate(paragraph.text, dest='es').text))
    for image in images:
        gallery_body.append(image.find("div", class_="gallery-image-container")['data-full-src'])
    title_es = translator.translate(article.find_all('a')[1].text, dest='es').text
    description_es = translator.translate(article.find('p').text, dest='es').text
    article = {"id": article['id'],
               "title": article.find_all('a')[1].text,
               "title_es": title_es,
               "image_source": article.find('img')['src'],
               "datetime": article.find('time')['datetime'],
               "description": article.find('p').text,
               "description_es": description_es,
               "text_body_es": body_es,
               "text_body": text_body,
               "gallery_body": gallery_body}
    print(article['id'])
    db.child("news").child(article['id']).set(article)