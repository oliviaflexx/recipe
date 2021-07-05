import csv
from fuzzywuzzy import fuzz
import re
import sqlite3

# Takes user input to categorize or ingredients and put in database
listy = []
with open('names.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        dicty = {}
        dicty['ingredient'] = row['ingredient']
        dicty['id'] = row['id']
        listy.append(dicty)

for ingredient in listy:
    if re.search('\Wor ', ingredient['ingredient']):
        for ing in listy:
            if re.search('\Wor ', ing['ingredient']):
                continue
            Token_Set_Ratio = fuzz.token_set_ratio(ingredient,ing)
            if Token_Set_Ratio > 90:
                first_name = ing['ingredient']
                second_name = ingredient['ingredient']
                while True:
                    print(f'PUT ({first_name}) IN ({second_name})?')
                    inputt = input('ANSWER:')
                    if inputt == 'y':
                        or_id = ingredient['id']
                        or_name = ingredient['ingredient']
                        in_id = ing['id']
                        in_name = ing['ingredient']
                        try:
                            sqliteConnection = sqlite3.connect('recipe.db')
                            cursor = sqliteConnection.cursor()

                            sqlite_insert_with_param = """INSERT INTO or_ingredients3
                                            (or_id, or_name, in_id, in_name) 
                                            VALUES (?, ?, ?, ?);"""

                            tuplee = (or_id, or_name, in_id, in_name)
                            cursor.execute(sqlite_insert_with_param, tuplee)
                            sqliteConnection.commit()
                            cursor.close()
                        except sqlite3.Error as error:
                            print("Failed to insert Python variable into sqlite table", error)
                        finally:
                            if sqliteConnection:
                                print('Success!')
                                sqliteConnection.close()
                                break
                    elif inputt == 'n':
                        break
