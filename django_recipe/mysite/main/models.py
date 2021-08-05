from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class recipes3(models.Model):
    name = models.CharField(max_length=200)
    time = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(max_length=200)
    image = models.CharField(max_length=200)
    calories = models.FloatField(null=True, blank=True)
    ingredients = models.ManyToManyField('ingredients3', related_name='recipes')
    genre = models.ManyToManyField('genres3', related_name='recipes')
    liked =models.ManyToManyField(User, related_name='liked')
    disliked =models.ManyToManyField(User, related_name='disliked')
    checked =models.ManyToManyField(User, related_name='checked')

    def __str__(self):
        return self.name

class ingredients3(models.Model):
    name = models.CharField(max_length=200)
    checked =models.ManyToManyField(User, related_name='ing_checked')
    or_ing = models.BooleanField(default=False)
    def __str__(self):
        return self.name
        
class genres3(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        
class recipe_ingredients3(models.Model):
    recipe = models.ForeignKey('recipes3', related_name='ingredient_amounts', on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey('ingredients3', related_name='ingredient_amounts', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f'RECIPE: {self.recipe.name} INGREDIENT: {self.ingredient.name}'

class or_ingredients(models.Model):
    or_name = models.ForeignKey('ingredients3', related_name='or_ingredient', on_delete=models.SET_NULL, null=True)
    in_name = models.ForeignKey('ingredients3', related_name='in_ingredient', on_delete=models.SET_NULL, null=True)

class user_recipes(models.Model):
    recipe = models.ForeignKey('recipes3', related_name='user_recipe', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", null=True)
    percent = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class grocery_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_list", null=True)
    name = models.ForeignKey('ingredients3', related_name='recipe_list', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



