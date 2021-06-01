from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import sys

# Open the page that lists all the recipes
with open('pretty.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'html.parser')
# find each post
    posts = soup.find_all('div', class_ = 'catpost')
    urls = []
    for post in posts:
        links = post.a['href']
        urls.append(links)
#initialize data storage
recipe_names = []
recipe_times = []
recipe_ingredients = []
linky = []

# For each url found...
for url in urls:    
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # Is the post a recipe?
    if not soup.find('div', class_ = 'post-recipe section'):
        continue
    recipe = soup.find('div', class_ = 'post-recipe section')
    # Does the post have a recipe name?
    if not recipe.find('h2', class_ = 'wprm-recipe-name wprm-block-text-bold'):
        continue
    recipe_name = recipe.find('h2', class_ = 'wprm-recipe-name wprm-block-text-bold').text
    recipe_names.append(recipe_name)
    # Does the post have a time?
    if not recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes'):
        continue
    recipe_time = recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes').text
    recipe_times.append(recipe_time)
    # Does the post have ingredients?
    if not recipe.find_all('span', class_ = 'wprm-recipe-ingredient-name'):
        continue
    recipe_ingredient = recipe.find_all('span', class_ = 'wprm-recipe-ingredient-name')
    i = 0
    for ingredient in recipe_ingredient:
        recipe_ingredient[i] = ingredient.text
        i = i + 1
    recipe_ingredients.append(recipe_ingredient)
    # Save the posts link
    linky.append(url)
    sleep(randint(2,10))

# Write the results to a text file
sys.stdout = open("eachlink.txt", "w")
print(recipe_names)
print(recipe_times)
print(recipe_ingredients)
print(linky)
sys.stdout.close()