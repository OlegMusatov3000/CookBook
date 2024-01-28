from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Product(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)
    times_used = models.SmallIntegerField('Кол-во использований', default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=255)
    products = models.ManyToManyField(
        Product, through='RecipeProduct',
        related_name='recipes', verbose_name='Продукты'
    )
    author = models.ForeignKey(
        User, related_name='recipes',
        verbose_name='Автор рецепта', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт', related_name='recipe_product'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт'
    )
    weight_in_grams = models.PositiveSmallIntegerField(
        'Количество в граммах',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Продукт рецепта'
        verbose_name_plural = 'Продукты рецепта'
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f'{self.product.name} для {self.recipe.name}'
