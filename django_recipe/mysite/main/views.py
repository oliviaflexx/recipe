from os import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_ingredients, user_recipes
import csv
from django import template

def index(response):
    return render(response, "main/home.html")

def allRecipes(response):
    recipes = recipes3.objects.all()
    recipe_ingredients = recipe_ingredients3.objects.all()
    return render(response, "main/allrecipes.html", {"recipes":recipes, 'recipe_ingredients':recipe_ingredients})

def ingredientPicker(response):
    if response.method == 'POST':
        if response.POST.get('save'):
            for ingredient in response.user.ingredients.all():
                if response.POST.get(str(ingredient.id)) == "touched":
                    ingredient.checked = True
                else:
                    ingredient.checked = False

                ingredient.save()
            recipes = recipes3.objects.all()
            user_recipes.objects.filter(user=response.user).delete()
            for recipe in recipes:
                counter = 0
                ingredients = recipe.ingredients.all()
                total = len(ingredients)
                for checked in user_ingredients.objects.filter(user=response.user, checked = True):
                    if ingredients.filter(name = checked.ingredient).exists():
                        counter = counter + 1
                percent = (counter / total) * 100
                entry = user_recipes.objects.create(recipe = recipe, user = response.user, percent = percent)
                entry.save()

            return redirect('/myrecipes')
    else:
        if response.user.is_authenticated:
            return render(response, "main/ingredient.html", {'user_ingredients': response.user.ingredients.all()})
        else:
            return redirect('/login')

def myrecipes(response):
    # user_recipe0 = user_recipes.objects.filter(percent > 0)
    user_recipes1 = response.user.recipes.filter(percent__gt=0).order_by('-percent')
    if response.method == 'POST':
        for user_recipe in user_recipes1:
            print(user_recipe.recipe)
            if response.POST.get('a' + str(user_recipe.recipe.id)):
                user_recipe.checked = True
                user_recipe.save()
                print(user_recipe.checked)
    return render(response, 'main/selected_recipes.html', {'user_recipes1': user_recipes1})

def groceryList(response):
    user_recipes1 = response.user.recipes.all()

    for user_recipe in user_recipes1:
        print(user_recipe.checked)
        if user_recipe.checked == True:
            ingredients = user_recipe.recipe.ingredient_amounts.all()
            for ingredient in ingredients:
                print(ingredient.ingredient)
                print(ingredient.amount)
                print(ingredient.unit)
    return render(response, 'main/grocery_list.html')

def addData(response):

    recipes3.objects.all().delete()
    ingredients3.objects.all().delete()
    recipe_ingredients3.objects.all().delete()
    or_ingredients.objects.all().delete()
    with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/names.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            ingredient = row['ingredient']
            entry = ingredients3(name=ingredient)
            entry.save()

    with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/recipes3.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            recipe_name = row['name']
            time = row['time']
            if time == '':
                time = 0
            url = row['url']
            image = row['image']
            calories = row['calories']
            if calories == '':
                calories = 0
            recipe = recipes3.objects.create(name=recipe_name,time=time,url=url,image=image,calories=calories)
            recipe.save()

            with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/recipe_ingredients.csv', mode='r') as ing_csv_file:
                ing_csv_reader = csv.DictReader(ing_csv_file)
                for ing_row in ing_csv_reader:
                    ing_recipe_name = ing_row['name']
                    ingredient = ing_row['ingredient']
                    amount = ing_row['amount']
                    if not amount:
                        amount = 0
                    unit = ing_row['unit']
                    if not unit:
                        unit = 'none'
                    if ing_recipe_name == recipe_name:
                        try:
                            ingredient_query = ingredients3.objects.get(name=ingredient)
                            recipe.ingredients.add(ingredient_query)
                            recipe_ingredients = recipe_ingredients3.objects.create(recipe=recipe, ingredient=ingredient_query, amount=amount, unit=unit)
                            recipe_ingredients.save()
                        except ingredients3.DoesNotExist:
                            print(ingredient)

            with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/genres.csv', mode='r') as genre_csv_file:
                genre_csv_reader = csv.DictReader(genre_csv_file)
                for genre_row in genre_csv_reader:
                    genre_recipe_name = genre_row['recipe_name']
                    genre = genre_row['genre']
                    if genre_recipe_name == recipe_name:
                        try:
                            genre_query = genres3.objects.get(name=genre)
                            recipe.genre.add(genre_query)
                        except genres3.DoesNotExist:
                            print(genre_recipe_name)

    with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/or_ingredients.csv', mode='r') as or_csv_file:
        or_csv_reader = csv.DictReader(or_csv_file)
        for or_row in or_csv_reader:
            or_name = or_row['or_name']
            or_name = ingredients3.objects.get(name=or_name)
            in_name = or_row['in_name']
            in_name = ingredients3.objects.get(name=in_name)
            entry = or_ingredients.objects.create(or_name=or_name, in_name=in_name)
            entry.save()
                    
    return HttpResponse("Data added")