from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from core.models import *


DEFAULT_MAX_LEN = 255


class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Article
        fields = ['title', 'slug', 'text','image','reading_time', 'cat']  #'image'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'where_to_repeat','oninput': "repeat('where_to_repeat, repeating')"}),
            'slug': forms.TextInput(attrs={'class': 'repeating'}),
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'password'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}))



    # title = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'where_to_repeat',
    #     'oninput': "repeat('where_to_repeat, repeating')"}), max_length=DEFAULT_MAX_LEN, label='Заголовок статьи')

    # slug = forms.SlugField(widget=forms.TextInput(attrs={
    #     'class': 'repeating'}), max_length=DEFAULT_MAX_LEN, label='URL', required=False)
    
    
    # text = forms.CharField(widget=forms.Textarea(
    #     attrs={'cols': 60, 'rows': 10}
    # ), label='Содержимое статьи')

    # image = forms.ImageField(label='Картинка', required=False)

    # is_publish = forms.BooleanField(label='Опубликовать', required=False, initial=True)
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Без категории', required=False)


    