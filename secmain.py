import requests
from bs4 import BeautifulSoup


raw_page = requests.get("http://www.cyclingnews.com/news/gerrans-im-not-racing-with-unfinished-business/")
data = raw_page.text
soup = BeautifulSoup(data, "html.parser")
body_page = soup.find("div", class_="post-page")
paragraphs = body_page.find_all("p")
images = soup.find_all("figure", class_="gallery-item")
for paragraph in paragraphs:
    print(paragraph.text)
for image in images:
    print(image.find("div", class_="gallery-image-container")['data-full-src'])
