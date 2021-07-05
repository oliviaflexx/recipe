import sqlite3

# Adds genres to database
try:
    sqliteConnection = sqlite3.connect('recipe.db')
    sqlite_create_table_query = """INSERT INTO genres3
                          (genre) 
                          VALUES (?);"""
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query, ('gluten free',))
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")