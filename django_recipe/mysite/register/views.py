from django.shortcuts import render, redirect
from .forms import RegisterForm
from main.models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_recipes
from django.contrib.auth import authenticate, login

# Create your views here.


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(response, new_user)
            return redirect("/home")
            
        return render(response, "register/register.html", {"form": form})
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

def logout(response):
    return render(response, 'registration/logout.html')
