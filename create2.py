import sqlite3

### Create table for Budget Bytes

# Create the recipe table
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE recipes2(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                time INTEGER,
                                time_unit TEXT,
                                url TEXT,
                                image TEXT,
                                calories INTEGER
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

# Create the ingredients table
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE ingredients2(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ingredient TEXT
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

# Create the association table
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE recipe_ingredients2(
                                recipes2_id INTEGER,
                                ingredients2_id INTEGER,
                                amount TEXT,
                                unit TEXT,
                                FOREIGN KEY(recipes2_id) REFERENCES recipes2(id),
                                FOREIGN KEY(ingredients2_id) REFERENCES ingredients2(id)
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