from django.db.models import Q, F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request):
    if request.method == 'GET':
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        product = get_object_or_404(Product, pk=product_id)

        recipe_product, created = RecipeProduct.objects.get_or_create(
            recipe=recipe,
            product=product,
            defaults={'weight_in_grams': weight}
        )

        if not created:
            recipe_product.weight_in_grams = weight
            recipe_product.save(update_fields=['weight_in_grams'])

        return HttpResponse('Product added to recipe successfully')

    return HttpResponse('Invalid request method')


def cook_recipe(request):
    if request.method == 'GET':
        recipe_id = request.GET.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        Product.objects.filter(recipeproduct__recipe=recipe).update(
            times_used=F('times_used') + 1
        )

        return HttpResponse('Recipe cooked successfully')

    return HttpResponse('Invalid request method')


def show_recipes_without_product(
        request, template='recipes/recipes_without_product.html'
):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        recipes = Recipe.objects.filter(
            ~Q(recipe_product__product=product) |
            Q(
                recipe_product__product=product,
                recipe_product__weight_in_grams__lt=10
            )
        )

        context = {
            'product': product,
            'recipes': recipes,
        }

        return render(request, template, context)

    return HttpResponse('Invalid request method')
