from core.models import Category
from django.db.models import Count

menu = [{'title': 'Главная', 'url_name':'home'},
        {'title': 'О сайте', 'url_name':'about'},
        {'title': 'Добавить статью', 'url_name': 'add_article'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('article'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)


        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context