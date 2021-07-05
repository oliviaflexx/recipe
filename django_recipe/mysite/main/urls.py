from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adddata/', views.addData, name="addData"),
    path('allrecipes/', views.allRecipes, name="allRecipes"),
    path('myrecipes/', views.myrecipes, name='myrecipes'),
    path('ingredients/', views.ingredientPicker, name='ingredientPicker'),
    path('home/',views.index, name='index'),
    path('grocerylist/', views.groceryList, name='groceryList')
]