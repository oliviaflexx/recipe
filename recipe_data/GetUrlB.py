import time
from selenium import webdriver
from bs4 import BeautifulSoup
import sys

# Budget Bytes url and image scraper
urls = []
photos = []
pages = list(range(1, 13))
for page in pages:
    if page == 1:
        page = "https://www.budgetbytes.com/category/recipes/"
    else:
        page ="https://www.budgetbytes.com/category/recipes/page/" + str(page) + '/'
    driver = webdriver.Chrome('/Users/oliviafelix/recipe-2/chromedriver')
    driver.get(page)  
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('div', class_ = 'post-image')
    for post in posts:
        # get url
        links = post.a['href']
        urls.append(links)
        # Get image
        images = post.img['src']
        photos.append(images)

sys.stdout = open("links2.txt", "w")
print(urls)
sys.stdout.close()

sys.stdout = open("images.txt", "w")
print(photos)
sys.stdout.close()
