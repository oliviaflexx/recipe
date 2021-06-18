import sys
from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import sqlite3
from datacleaner import clean
import csv
from fuzzywuzzy import fuzz

## Budget bytes database entry USING CSV ##

def insertFoodIntoIngredients(food):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()

        sqlite_fuzzy = """SELECT ingredient FROM ingredients3;"""

        sqlite_select_food_with_param = """SELECT id FROM ingredients3
                        WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO ingredients3
                          (ingredient) 
                          VALUES (?);"""

        data_tuple = (food,)

        cursor.execute(sqlite_fuzzy)
        sqliteConnection.commit()
        ingredient_list = cursor.fetchall()

        cursor.execute(sqlite_select_food_with_param, data_tuple)
        sqliteConnection.commit()
        food_id = cursor.fetchone()

        if food_id == None:
            isit = 'no'
            for match in ingredient_list:
                Token_Sort_Ratio = fuzz.token_sort_ratio(food,match[0])
                if Token_Sort_Ratio == 100:
                    print(food, match[0])
                    food = match[0]
                    isit = 'yes'

            if isit == 'no':
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return food

def selectFood(recipe_name, food, amount, unit):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()

        sqlite_select_recipe_with_param = """SELECT id FROM recipes3 WHERE name = ?;"""

        sqlite_select_food_with_param = """SELECT id FROM ingredients3
                          WHERE ingredient = ?;"""

        sqlite_insert_with_param = """INSERT INTO recipe_ingredients3
                          (recipes3_id, ingredients3_id, amount, unit) 
                          VALUES (?, ?, ?, ?);"""

        tuplee = (recipe_name,)
        cursor.execute(sqlite_select_recipe_with_param, tuplee)
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

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

with open('OLDfullRecipe.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        result = clean(row['ingredient'], row['amount'], row['unit'])
        if result[0] is None:
            continue
        ingredient_name = insertFoodIntoIngredients(result[0])
        selectFood(row['recipe'], ingredient_name, result[1], result[2])
