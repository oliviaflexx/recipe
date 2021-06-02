import sqlite3

def insertVaribleIntoTable(name, time, url, image):
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

insertVaribleIntoTable('cupcake', 30, 'www.cupcake.com', 'www.imagecupcake.com')
insertVaribleIntoTable('cupcake2', 20, 'www.cupcake2.com', 'www.imagecupcake2.com')