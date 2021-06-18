import sys
from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import sqlite3

### Puts the jessica recipes into the database

# Clean up the links
links = []
f = open("links.txt", "r")
links = f.readline()
new_links = links.replace('[', '')
new_links = new_links.replace(']', '')
final_links = new_links.split(', ')

counter = 0
images = []

# Put the recipe data into the table
def insertVariableIntoTable(name, time, url, image):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO recipe
                          (name, time, url, image) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (name, time, url, image)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into recipe")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
# Put the ingredient data into the table
def insertFoodIntoTable(food):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_food_with_param = """SELECT id FROM ingredients
                        WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO ingredients
                          (ingredient) 
                          VALUES (?);"""

        data_tuple = (food,)

        cursor.execute(sqlite_select_food_with_param, data_tuple,)
        sqliteConnection.commit()
        food_id = cursor.fetchone()
        if food_id == None:
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("Python Variables inserted successfully into ingredients")
        else:
            print("Already existed")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

# Link the two tables with the association table
def selectFood(food):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_recipe_with_param = """SELECT id FROM recipe ORDER BY id DESC LIMIT 1;"""

        sqlite_select_food_with_param = """SELECT id FROM ingredients
                          WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO recipe_ingredients
                          (recipe_id, ingredient_id) 
                          VALUES (?, ?);"""

        cursor.execute(sqlite_select_recipe_with_param)
        sqliteConnection.commit()
        recipe_id0 = cursor.fetchone()
        middle = ''.join(map(str, recipe_id0))
        recipe_id = int(middle)

        data_tuple = (food,)
        cursor.execute(sqlite_select_food_with_param, data_tuple)
        sqliteConnection.commit()
        food_id0 = cursor.fetchone()
        middle = ''.join(map(str, food_id0))
        food_id = int(middle)

        final_tuple = (recipe_id, food_id)
        cursor.execute(sqlite_insert_with_param, final_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into recipe_ingredients")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

# Get images for each post
with open('pretty.html', 'r') as html_file:
    content = html_file.read()
    soup0 = BeautifulSoup(content, 'html.parser')

    imagebox = soup0.find_all('div', class_ = 'imgbox')
    for image in imagebox:
        print(image)
        try:
            img = image.img['src']
            images.append(img)
        except:
            images.append(0)

for link in final_links:
    new_link = link.strip('\'')
    html_text = requests.get(new_link).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # Not a recipe
    if not soup.find('div', class_ = 'post-recipe section'):
        recipe_image = None
        recipe_name = None
        recipe_time = None
        link = None
    else:
        recipe = soup.find('div', class_ = 'post-recipe section')

        # no name
        if not recipe.find('h2', class_ = 'wprm-recipe-name wprm-block-text-bold'):
            recipe_name = None
        else: 
            recipe_name = recipe.find('h2', class_ = 'wprm-recipe-name wprm-block-text-bold').text
            # No image
            if images[counter] == 0:
                recipe_image = None
            else:
                recipe_image = images[counter]
        # No time
        if not recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes'):
            recipe_time = None
        else:
            recipe_time = recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes').text
        
        insertVariableIntoTable(recipe_name, recipe_time, link, recipe_image)

        # Find ingredients
        recipe_ingredient = recipe.find_all('span', class_ = 'wprm-recipe-ingredient-name')
        for ingredient in recipe_ingredient:
            food = ingredient.text
            insertFoodIntoTable(food)
            selectFood(food)
    counter = counter + 1
    sleep(randint(2,10))
