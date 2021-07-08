from django.shortcuts import render, redirect
from .forms import RegisterForm
from main.models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_ingredients, user_recipes
from django.contrib.auth import authenticate, login

# Create your views here.


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(response, new_user)
            # Make their ingredient list now so it can be faster later
            ingredients = ingredients3.objects.all().order_by('name')
            for ingredient in ingredients:
                if or_ingredients.objects.filter(or_name=ingredient).exists():
                    entry = user_ingredients.objects.create(
                        user=new_user, ingredient=ingredient, checked=False, or_ingredient=True)
                else:
                    entry = user_ingredients.objects.create(
                        user=new_user, ingredient=ingredient, checked=False, or_ingredient=False)
                entry.save()
            
            recipes = recipes3.objects.all()
            for recipe in recipes:
                user_recipes.objects.create(user=new_user, recipe=recipe)
        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

def logout(response):
    return render(response, 'registration/logout.html')
