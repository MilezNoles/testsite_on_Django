from django import forms
from .models import News, Comments  # для выпадающего списка категорий
import re  # для clean_title
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label="Тема",
                              widget=forms.TextInput(attrs={'class': "form-control", }), )
    content = forms.CharField(label="Текст",
                              widget=forms.Textarea(attrs={'class': "form-control", 'rows': 5}), )
    captcha = CaptchaField()


class UserLogin(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя",
                               widget=forms.TextInput(attrs={'class': "form-control", }), )
    password = forms.CharField(label="Введите пароль",
                               widget=forms.PasswordInput(attrs={'class': "form-control", }))


class UserRegister(UserCreationForm):
    username = forms.CharField(label="Имя пользователя",
                               widget=forms.TextInput(attrs={'class': "form-control", }),
                               help_text="Должно состоять не более чем из 150 символов")
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': "form-control", }))
    password1 = forms.CharField(label="Введите пароль", widget=forms.PasswordInput(attrs={'class': "form-control", }),
                                help_text="Не менее 8 символов(буквы и цифры)")
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={'class': "form-control", }))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # widgets = {"username" : forms.TextInput(attrs={'class': "form-control", }),
        #            "email": forms.EmailInput(attrs={'class': "form-control", }),
        #            "password1" : forms.PasswordInput(attrs={'class': "form-control", }),
        #            "password2": forms.PasswordInput(attrs={'class': "form-control", }),
        #
        # } для UserCreationForm это поле работает не корректно, поэтому все переносим из меты в UserRegister


class NewsForm(forms.ModelForm):
    class Meta:
        model = News  # из какой модели
        # fields = "__all__"      # какие поля (all) все
        fields = ["title", "content", "is_published", "category"]
        widgets = {
            "title": forms.TextInput(attrs={'class': "form-control", }),
            "content": forms.Textarea(attrs={
                'class': "form-control",
                'rows': 5
            }),
            "category": forms.Select(attrs={'class': "form-control", }),

        }

    def clean_title(self):  # валидатор для title
        title = self.cleaned_data["title"]
        if re.match(r"\d", title):  # \d цифра
            raise ValidationError("Название новости не должно начинаться с цифры")
        return title

    def clean_is_published(self):  # валидатор для is_published
        is_published = self.cleaned_data["is_published"]
        if is_published == False:
            raise ValidationError("Новость неопубликована")
        return is_published


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["nickname", "message", ]
        widgets = {
            "nickname": forms.TextInput(attrs={'class': "form-control", "type": "hidden"}, ),
            "message": forms.Textarea(attrs={
                'class': "form-control",
                'rows': 5
            }),

        }
