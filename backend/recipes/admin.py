from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Product, Recipe, RecipeProduct

admin.site.unregister(Group)

User = get_user_model()


class RecipeProductInline(admin.StackedInline):
    model = RecipeProduct
    extra = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.parent_model.__name__ == 'Product':
            self.verbose_name_plural = (
                'В каких рецептах используется:'
            )
        else:
            self.verbose_name_plural = 'Продукты:'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'name', 'times_used')
    search_fields = ('name',)
    readonly_fields = ('times_used',)
    inlines = (RecipeProductInline,)
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'name', 'author')
    list_filter = ('author',)
    search_fields = ('name',)
    inlines = (RecipeProductInline,)
    exclude = ('author',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
