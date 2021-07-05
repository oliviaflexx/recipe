import sys
import sqlite3
import csv
from typing import KeysView

# ADD UP ALL THE INGREDIENT AMOUNTS
def get(ingredient_id):
    try:
        dicty = {}
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()

        get_ingredients = """SELECT amount, unit, ingredients3_id FROM recipe_ingredients3 WHERE ingredients3_id = ?;"""
        
        get_name = """SELECT ingredient FROM ingredients3 WHERE id = ?;"""

        data_tuple = (ingredient_id,)

        cursor.execute(get_name, data_tuple)
        sqliteConnection.commit()
        name = cursor.fetchone()

        cursor.execute(get_ingredients, data_tuple)
        sqliteConnection.commit()
        amount_unit_list = cursor.fetchall()

        for tup in amount_unit_list:
            try:
                amount = float(tup[0])
            except ValueError:
                print(tup[0])
                continue
            unit = tup[1]
            if unit == '':
                unit = name[0]
            try:
                old_amount = dicty[unit]
                dicty[unit] = amount + old_amount
            except KeyError:
                dicty[unit] = amount

    except sqlite3.Error as error:
        print("Failed to get Python variable from sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    return name[0], dicty


with open('test.csv', mode='a') as names_file:
    names_writer = csv.writer(names_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in range(1, 966):
        diccy = get(x)
        tuplee = (diccy[0], diccy[1])
        names_writer.writerow(tuplee)
    names_file.close()