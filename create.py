import sqlite3

# Tables creating for jessica
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE recipe_ingredients(
                                recipe_id INTEGER,
                                ingredient_id INTEGER,
                                FOREIGN KEY(recipe_id) REFERENCES recipe(id),
                                FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
                                );'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")
