from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

MODEL = models.Model
DEFAULT_MAX_LEN = 255






class Category(MODEL):
    title = models.CharField(verbose_name='Заголовок', max_length=100, db_index=True)
    slug = models.SlugField(max_length=DEFAULT_MAX_LEN, unique=True, db_index=True, verbose_name="URL")
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Article(MODEL):
    title = models.CharField('Заголовок', max_length=DEFAULT_MAX_LEN)
    slug = models.SlugField(max_length=DEFAULT_MAX_LEN, unique=True, db_index=True, verbose_name="URL")
    
    text = models.TextField('Текст')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    image = models.ImageField('Картинка', null=True, upload_to='resource')

    created_date = models.DateField('Дата публикации', auto_now_add=True)
    reading_time = models.IntegerField('Время на чтение', default=5, null=True)

    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", null=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('article', kwargs={'post_slug': self.slug})


    class Meta:
        ordering = ('id',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


