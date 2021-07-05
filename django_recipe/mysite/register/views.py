from django.shortcuts import render, redirect
from .forms import RegisterForm
from main.models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_ingredients

# Create your views here.


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            # Make their ingredient list now so it can be faster later
            ingredients = ingredients3.objects.all().order_by('name')
            for ingredient in ingredients:
                entry = user_ingredients.objects.create(
                    user=response.user, ingredient=ingredient, checked=False)
                entry.save()
        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
