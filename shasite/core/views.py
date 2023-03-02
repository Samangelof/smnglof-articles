from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login


from core.models import *
from core.forms import *
from core.utils import *


# Добавление в избранное


menu = [{'title': 'Главная', 'url_name':'home'},
        {'title': 'О сайте', 'url_name':'about'},
        {'title': 'Добавить статью', 'url_name': 'add_article'},
        {'title': 'Войти', 'url_name': 'auth'}]






class MainHome(DataMixin, ListView):
    model = Article
    template_name: str = 'main.html'
    context_object_name: str = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')

        return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return Article.objects.filter(is_published=True)       



# def index(request):
#     posts = Article.objects.all()
#     context = {
#         'posts': posts, 
#         'menu': menu, 
#         'title': 'Главная страница',
#         'cat_selected': 0,
#         }
#     return render(request, 'index.html', context=context)


#================================================================================
# Не класс, не наследует DataMixin. 
# Поэтому при переходе на эндпоинт: 'about/'
# он показывает ссылку на 'Добавить статью', 
# при наличии класса он не будет этого делать, пока юзер не авторизован
# Следует переписать функцию на класс

def about(request):
    return render(request, 'about.html', {'menu': menu, 'title': 'О сайте'})
#================================================================================



class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddArticleForm
    template_name: str = 'add_article.html'
    success_url = reverse_lazy('thanks')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        
        return dict(list(context.items()) + list(c_def.items()))



# def add_article(request):
#     if request.method == 'POST':
#         form = AddArticleForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             try:
#                 Article.objects.create(**form.cleaned_data)
#                 return redirect('/main/')
#             except Exception as Err:
#                 form.add_error(None, f'[ERROR]: {Err}')
#     else:
#         form = AddArticleForm()
#     return render(request, 'add_article.html',  {'form': form, 'menu': menu, 'title': 'Добавить статью'})









class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name: str = 'register.html'
    success_url = reverse_lazy('auth')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

# def login(request):
#     return HttpResponse('Страница авторизации')


def send_letter(request):
    return render(request, 'send.html')
    


class AuthUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('register')







class Thanks(ListView):
    model = Article
    template_name: str = 'thanks.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
        
# def thank_you(request):
#     template = 'thanks.html'
#     context = {}
#     return render(request, template, context)






class ShowArticle(DataMixin, DetailView):
    model = Article
    template_name: str = 'post.html'
    slug_url_kwarg: str = 'post_slug'
    # pk_url_kwarg: str = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        
        return dict(list(context.items()) + list(c_def.items()))





class ArticleCategory(DataMixin, ListView):
    model = Article
    template_name: str = 'main.html'
    context_object_name: str = 'posts'
    allow_empty: bool = False

    def get_queryset(self):
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Категория: ' + str(context['posts'][0].cat),
            cat_selected=context['posts'][0].cat_id
            )
        

        return dict(list(context.items()) + list(c_def.items()))





def show_category(request, cat_id):
    posts = Article.objects.filter(cat_id=cat_id)
    
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts, 
        'menu': menu, 
        'title': 'Главная страница',
        'cat_selected': cat_id,
        }
    return render(request, 'main.html', context=context)








def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<br>ERROR 404</h1>')