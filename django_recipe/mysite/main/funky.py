from .models import or_ingredients, recipe_ingredients3, recipes3, ingredients3, genres3, user_ingredients, user_recipes, grocery_list

def add_up(user_recipe, the_user):
    user_recipe.checked = True
    user_recipe.save()
    # p = inflect.engine()
    ingredients = user_recipe.recipe.ingredient_amounts.all()
    for ingredient in ingredients:
        ingredient_name = ingredient.ingredient
        ingredient_amount = ingredient.amount
        ingredient_unit = ingredient.unit
        if grocery_list.objects.filter(user=the_user,name=ingredient_name, unit=ingredient_unit).exists():
            model_ing = grocery_list.objects.get(user=the_user,name=ingredient_name, unit=ingredient_unit)
            total_amount = float(model_ing.amount) + float(ingredient_amount)
            if total_amount > 1:
                # model_ing.name =p.plural(model_ing.name)
                # model_ing.unit = p.plural(model_ing.unit)
                pass
            model_ing.amount = total_amount
            #### its not updating its adding, should check if recipe is already in recipe list
        else:
            if ingredient_amount > 1:
                # ingredient_name = p.plural(ingredient_name)
                # ingredient_unit = p.plural(ingredient_unit)
                pass
            model_ing = grocery_list.objects.create(user=the_user,name=ingredient_name, unit=ingredient_unit,amount=ingredient_amount)
        model_ing.save()

def sub_out(user_recipe, the_user):
    user_recipe.checked = False
    user_recipe.save()
    ingredients = user_recipe.recipe.ingredient_amounts.all()
    for ingredient in ingredients:
        ingredient_name = ingredient.ingredient
        ingredient_amount = ingredient.amount
        ingredient_unit = ingredient.unit
        if grocery_list.objects.filter(user=the_user,name=ingredient_name, unit=ingredient_unit, amount=ingredient_amount).exists():
            model_ing = grocery_list.objects.get(user=the_user,name=ingredient_name, unit=ingredient_unit, amount=ingredient_amount).delete()
        else:
            model_ing = grocery_list.objects.get(user=the_user,name=ingredient_name, unit=ingredient_unit)
            total_amount = float(model_ing.amount) - float(ingredient_amount)
            if total_amount <= 1:
                #### model_ing.name =p.singular(model_ing.name)
                #### model_ing.unit = p.singular(model_ing.unit)
                pass
            model_ing.amount = total_amount
            model_ing.save()