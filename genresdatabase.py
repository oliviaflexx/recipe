import sqlite3
import time
from selenium import webdriver
from bs4 import BeautifulSoup

## Budget bytes genre database entry ##

def insertRecipeIntoGenres(title):
    try:
        sqliteConnection = sqlite3.connect('recipe.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_recipe_with_param = """SELECT id FROM recipes3
                        WHERE name = ?;"""

        sqlite_insert_with_param = """INSERT INTO recipe_genres3
                          (recipes3_id, genres3_id) 
                          VALUES (?, ?);"""

        data_tuple = (title,)

        cursor.execute(sqlite_select_recipe_with_param, data_tuple)
        sqliteConnection.commit()
        recipe_id = cursor.fetchone()
        print(recipe_id)
        if recipe_id:
            other_tuple = (recipe_id[0], '5')
            cursor.execute(sqlite_insert_with_param, other_tuple)
            sqliteConnection.commit()
            print("Success")
        else:
            print("No recipe")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

pages = list(range(1,6))
for page in pages:
    if page == 1:
        page = "https://www.budgetbytes.com/category/recipes/gluten-free/"
    else:
        page = "https://www.budgetbytes.com/category/recipes/gluten-free/page/" + str(page) + '/'
    driver = webdriver.Chrome('/Users/oliviafelix/recipe-2/chromedriver')
    driver.get(page)  
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('div', class_ = 'post-image')
    for post in posts:
        title = post.a['title']
        insertRecipeIntoGenres(title)
