from os import name
from django.db.models.query import QuerySet, Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_ingredients, user_recipes, grocery_list
import csv
from django import template
import inflect
from .funky import add_up, sub_out
from django.core.paginator import Paginator
import json

def index(response):
    return render(response, "main/home.html")

def show(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        recipe = recipes3.objects.get(id=id)

        if request.POST.get('shown') == 'Show Less':
            result = 'Show More'
            calories = ''
            time = ''
            genres = ''
            print(result)
        else:
            genres_list = []
            calories = 'Calories: ' + str(recipe.calories)
            time = 'Time: ' + str(recipe.time) + ' Minutes'
            for genre in recipe.genre.all():
                genres_list.append(genre.name)
            if len(genres_list) == 0:
                genres = ''
            else:
                genres = 'Genres: ' + str(genres_list)
            result = 'Show Less'
            print(result)
        return JsonResponse({'result': result, 'id': recipe.id, 'calories': calories, 'time': time, 'genres': genres })

def like(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        user_recipe = user_recipes.objects.get(user=request.user, id=id)
        print(user_recipe.recipe.name)
        if user_recipe.liked == True:
            user_recipe.liked = False
            user_recipe.save()
            print('unliked')
            result = 'unliked'
        else:
            user_recipe.liked = True
            user_recipe.disliked = False
            user_recipe.save()
            result = 'liked'
            print('liked')

        return JsonResponse({'id': user_recipe.id, 'result': result})

def dislike(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        user_recipe = user_recipes.objects.get(user=request.user, id=id)
        print(user_recipe.recipe.name)
        if user_recipe.disliked == True:
            user_recipe.disliked = False
            user_recipe.save()
            print('undisliked')
            result = 'undisliked'
        else:
            user_recipe.disliked = True
            user_recipe.liked = False
            user_recipe.save()
            print('disliked')
            result = 'disliked'

        return JsonResponse({'result': result, 'id': user_recipe.id})


def add_recipe(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('postid')
        recipe = recipes3.objects.get(id=id)
        print(recipe.name)
        print(request.POST.get('checked'))
        user_recipe = user_recipes.objects.get(user=request.user, recipe=recipe)

        if request.POST.get('checked') == 'Remove From Grocery List':
            print('disliked')
            result = 'Add to Grocery List'
            sub_out(user_recipe, request.user)
            print(result)
        else:
            print('liked')
            result = 'Remove From Recipe List'
            add_up(user_recipe, request.user)
            print(result)

        return JsonResponse({'result': result, 'id':id})

def allRecipes(response):
    if response.user.is_authenticated:

        if response.method == 'POST':
            posts = user_recipes.objects.select_related('recipe').filter(user=response.user).order_by('id')
            if response.POST.get('save'):
                genres = genres3.objects.all()
                if response.POST.__contains__('meal_type'):
                    meal0 = response.POST.get('meal_type')
                    if meal0 =='lunch':
                        breakfast = genres.get(name='breakfast')
                        dessert = genres.get(name='dessert')
                        posts = posts.exclude(recipe__genre=breakfast).exclude(recipe__genre=dessert)
                    else:
                        # meal = genres3.objects.get(name=meal0)
                        meal = genres.get(name=meal0)
                        posts = posts.filter(recipe__genre=meal.id)

                if response.POST.__contains__('restrict'):
                    restricts = response.POST.getlist('restrict')
                    for restrict in restricts:
                        if restrict == 'gluten':
                            restrict = 'gluten free'
                        restricter = genres.get(name=restrict)
                        posts = posts.filter(recipe__genre=restricter)

                if response.POST.__contains__('orderby'):
                    order = response.POST.get('orderby')
                    if order == 'calories':
                        posts = posts.exclude(recipe__calories=0).order_by('recipe__calories')
                    else:
                        posts = posts.exclude(recipe__time=0).order_by('recipe__time')
                else:
                    posts = posts.order_by('id')

            paginator = Paginator(posts, 25)
            page = response.GET.get('page')
            posts = paginator.get_page(page)

            return render(response, "main/allrecipes.html", {'posts':posts})
        
        else:
            posts = user_recipes.objects.select_related('recipe').filter(user=response.user).order_by('recipe__name')
            paginator = Paginator(posts, 25)
            page = response.GET.get('page')
            posts = paginator.get_page(page)

            return render(response, "main/allrecipes.html", {'posts':posts})
    else:
        return render(response, "main/allrecipes.html")


def ingredientPicker(response):
    if response.method == 'POST':
        if response.POST.get('save'):
            # print(response.POST)
            selected_ingredients = response.POST.getlist('touched')
            db_ingredients = user_ingredients.objects.select_related('ingredient').filter(user=response.user)
            for sel_ing in selected_ingredients:
                ingredient = db_ingredients.get(pk=sel_ing)
                ingredient.checked = True
                if or_ingredients.objects.filter(in_name=ingredient.ingredient).exists():
                    print('exists')
                    for or_name in or_ingredients.objects.filter(in_name=ingredient.ingredient):
                        recipes0 = recipe_ingredients3.objects.filter(ingredient=or_name.or_name)
                        for recipe0 in recipes0:
                            print(f'OR:', recipe0.recipe)   
                        thing = db_ingredients.get(ingredient=or_name.or_name)
                        print(f'CHECKED BEFORE:', thing.ingredient.name, thing.checked)
                        thing.checked = True
                        thing.save()
                        print(f'CHECKED AFTER:', thing.checked)
                ingredient.save()

            recipe_list = []
            for sel_ing in selected_ingredients:
                ingredient = db_ingredients.get(pk=sel_ing)
                recipes = recipe_ingredients3.objects.select_related('recipe').filter(ingredient = ingredient.ingredient)
                for recipe in recipes:
                    recipe_list.append(recipe.recipe)

            users = user_recipes.objects.filter(user=response.user)
            for user in users:
                user.percent = None

            recipe_dict = {}
            for recipe in recipe_list:
                try:
                    recipe_dict[recipe] = recipe_dict[recipe] + 1
                except KeyError:
                    recipe_dict.update({recipe: 1})
            
            for key in recipe_dict:
                total = key.ingredients.all().count()
                percent = (recipe_dict[key] / total) * 100
                entry = user_recipes.objects.get(recipe = key, user = response.user)
                entry.percent = percent
                entry.save()

            return redirect('/myrecipes')

    else:
        if response.user.is_authenticated:
            # user_recipes.objects.all().delete()
            # user_ingredients.objects.all().delete()
            non_ors = user_ingredients.objects.select_related('ingredient').filter(user=response.user,or_ingredient=False)
            return render(response, "main/ingredient.html", {'non_ors': non_ors})
        else:
            return redirect('/login')

def myrecipes(response):
    if response.user.is_authenticated:
        # user_recipe0 = user_recipes.objects.filter(percent > 0)
        user_recipes1 = response.user.recipes.select_related('recipe').exclude(percent__isnull=True).order_by('-percent')
        return render(response, 'main/selected_recipes.html', {'user_recipes1': user_recipes1})
    else:
        return render(response, 'main/selected_recipes.html')

def liked_recipes(response):
    if response.user.is_authenticated:
        # user_recipe0 = user_recipes.objects.filter(percent > 0)
        user_recipes1 = response.user.recipes.select_related('recipe').exclude(liked=False)
        return render(response, 'main/selected_recipes.html', {'user_recipes1': user_recipes1})
    else:
        return render(response, 'main/selected_recipes.html')

def groceryList(response):
    # grocery_list.objects.all().delete()
    if response.user.is_authenticated:
        return render(response, 'main/grocery_list.html', {'ingredients': grocery_list.objects.filter(user=response.user).order_by('name__name'), 'recipes': user_recipes.objects.filter(user=response.user,checked=True)})
    else:
        return render(response, 'main/grocery_list.html')


def addData(response):
    if response.method == 'POST':
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
                url = row['url'].replace('\'','')
                print(url)
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
                            amount = None
                        unit = ing_row['unit']
                        if not unit:
                            unit = None
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
    else:
        return render(response, 'main/add_data.html')