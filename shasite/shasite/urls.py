from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls, name='father'), #Удалить имя
    path('home/', views.MainHome.as_view(), name='home'),
    path('', views.MainHome.as_view()),
    path('about/', views.about, name='about'),
    path('add_article/', views.AddArticle.as_view(), name='add_article'),
    
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('auth/', views.AuthUser.as_view(), name='auth'),


    path('article/<slug:post_slug>/', views.ShowArticle.as_view(), name='article'),
    path('category/<slug:cat_slug>/', views.ArticleCategory.as_view(), name='category'),

    path('gratitude/', views.Thanks.as_view(), name='thanks'),

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.pageNotFound