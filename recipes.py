from bs4 import BeautifulSoup
import sys

# open the page of recipes
with open('pretty.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'html.parser')

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