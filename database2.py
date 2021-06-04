import sys
from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import sqlite3

# Budget bytes database entry

# clean the links up
links = []
f = open("links2.txt", "r")
links = f.readline()
final_links = links.replace('[', '').replace(']', '').split(', ')

# clean the images up
images = []
f = open("images.txt", "r")
images = f.readline()
final_images = images.replace('[', '').replace(']', '').split(', ')

for link in final_links:
    # take out the extra quotation marks
    new_link = link.strip('\'')

def insertInfoIntoRecipe(name, time, url, image, calories):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO recipes2
                          (name, time, url, image, calories) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (name, time, url, image, calories)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into recipes2")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
def insertFoodIntoIngredients(food):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_food_with_param = """SELECT id FROM ingredients2
                        WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO ingredients2
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

def selectFood(food, amount, unit):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_recipe_with_param = """SELECT id FROM recipes2 ORDER BY id DESC LIMIT 1;"""

        sqlite_select_food_with_param = """SELECT id FROM ingredients2
                          WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO recipe_ingredients2
                          (recipes2_id, ingredients2_id, amount, unit) 
                          VALUES (?, ?, ?, ?);"""

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

        final_tuple = (recipe_id, food_id, amount, unit)
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

counter = 0

for link in final_links:
    new_link = link.strip('\'')
    new_image = final_images[counter].strip('\'')
    html_text = requests.get(new_link).text
    soup = BeautifulSoup(html_text, 'html.parser')
 
    if not soup.find('div', class_ = 'wprm-recipe wprm-recipe-template-custom'):
        counter = counter + 1
        continue
    recipe = soup.find('div', class_ = 'wprm-recipe wprm-recipe-template-custom')
    recipe_image = new_image
    try:
        recipe_name = recipe.find('h2', class_ = 'wprm-recipe-name wprm-block-text-bold').text
    except AttributeError:
        recipe_name = None

    try:
        minutes = recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes').text
        try:
            hours = recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-hours wprm-recipe-total_time wprm-recipe-total_time-hours').text
            total = (int(hours) * 60 + int(minutes))
            recipe_time = total
        except AttributeError:
            recipe_time = minutes
    except AttributeError:
        try:
            hours = recipe.find('span', class_ = 'wprm-recipe-details wprm-recipe-details-hours wprm-recipe-total_time wprm-recipe-total_time-hours').text
            recipe_time = int(hours) * 60
        except AttributeError:
            recipe_time = None
    
    # find calories
    try:
        nutritions = recipe.find_all('span', class_ = 'wprm-nutrition-label-text-nutrition-value')
        calories = nutritions[1].text
    except IndexError:
        calories = None

    insertInfoIntoRecipe(recipe_name, recipe_time, link, recipe_image, calories)

    recipe_ingredient = soup.find_all('li', class_ = 'wprm-recipe-ingredient')
    for ingredient in recipe_ingredient:
        try:
            amount = ingredient.find('span', class_ = 'wprm-recipe-ingredient-amount').text
        except AttributeError:
            amount = None
        try:
            unit = ingredient.find('span', class_ = 'wprm-recipe-ingredient-unit').text
        except AttributeError:
            unit = None

        food = ingredient.find('span', class_ = 'wprm-recipe-ingredient-name').text
        insertFoodIntoIngredients(food)
        selectFood(food, amount, unit)

    counter = counter + 1
    sleep(randint(2,10))
