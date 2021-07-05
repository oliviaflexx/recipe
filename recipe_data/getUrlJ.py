import time
from selenium import webdriver
from bs4 import BeautifulSoup
import sys

##### Web scrapper for jessica infinite scrolling page, returns the html #####
driver = webdriver.Chrome('/Users/oliviafelix/Desktop/testing/chromedriver')
driver.get("https://jessicainthekitchen.com/recipes/")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 3 # You can set your own pause time
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

# Get HTML 
soup0 = BeautifulSoup(driver.page_source, 'html.parser')
soup = soup0.prettify()

# From each post get a url
posts = soup.find_all('div', class_ = 'catpost')
urls = []
for post in posts:
    links = post.a['href']
    urls.append(links)

# Write the urls to the links.txt
sys.stdout = open("links.txt", "w")
print(urls)
sys.stdout.close()
