from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('adddata/', views.addData, name="addData"),
    path('allrecipes/', views.allRecipes, name="allRecipes"),
    path('myrecipes/', views.myrecipes, name='myrecipes'),
    path('ingredients/', views.ingredientPicker, name='ingredientPicker'),
    path('home/',views.index, name='index'),
    path('grocerylist/', views.groceryList, name='groceryList'),
    path('like/', views.like, name='like'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('liked_recipes/',views.liked_recipes, name='liked_recipes'),
    path('showmore/',views.showmore, name='showmore'),
    path('dislike/', views.dislike, name='dislike'),
    path('add_ingredient/', views.add_ingredient, name="add_ingredient"),
    path('checky/', views.checky, name="checky"),
]