import sqlite3

### Create table for Budget Bytes

# Create the recipe table
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE recipes3(
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
    sqlite_create_table_query = '''CREATE TABLE ingredients3(
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
    sqlite_create_table_query = '''CREATE TABLE recipe_ingredients3(
                                recipes3_id INTEGER,
                                ingredients3_id INTEGER,
                                amount TEXT,
                                unit TEXT,
                                FOREIGN KEY(recipes3_id) REFERENCES recipes3(id),
                                FOREIGN KEY(ingredients3_id) REFERENCES ingredients3(id)
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

try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE or_ingredients3(
                                or_id INTEGER,
                                or_name TEXT NOT NULL,
                                in_id INTEGER,
                                in_name TEXT NOT NULL,
                                FOREIGN KEY(or_id) REFERENCES recipes3(id),
                                FOREIGN KEY(in_id) REFERENCES recipes3(id)
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

try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE genres3(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                genre TEXT
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

try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = '''CREATE TABLE recipe_genres3(
                                recipes3_id INTEGER,
                                genres3_id INTEGER,
                                FOREIGN KEY(recipes3_id) REFERENCES recipes3(id),
                                FOREIGN KEY(genres3_id) REFERENCES genres3(id)
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
