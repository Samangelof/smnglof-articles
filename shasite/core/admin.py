from django.contrib import admin
from core.models import Article, Category


@admin.register(Article)
@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
