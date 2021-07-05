from django.contrib import admin
from .models import recipe_ingredients3, recipes3, ingredients3, genres3, or_ingredients,user_ingredients, user_recipes, recipe_list
# Register your models here.
admin.site.register(recipes3)
admin.site.register(ingredients3)
admin.site.register(genres3)
admin.site.register(recipe_ingredients3)
admin.site.register(or_ingredients)
admin.site.register(user_ingredients)
admin.site.register(user_recipes)
admin.site.register(recipe_list)