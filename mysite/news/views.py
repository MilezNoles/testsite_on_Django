from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from django.contrib.auth import login, logout
from .utils import *
from django.core.mail import send_mail

from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)  # связь формы с данными
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(get_mail_subject(form.cleaned_data["username"]),
                      get_mail_context(form.cleaned_data["username"], form.cleaned_data["email"],
                                       form.cleaned_data["password1"]),
                      "testsubj88@yandex.ru", ["sgrimj@gmail.com", form.cleaned_data["email"]],
                      fail_silently=False)
            messages.success(request,
                             "Вы успешно зарегистрировались, письмо с данными было отправлено на вашу почту")
            return redirect("home")
        else:
            messages.error(request, "Ошибка регистрации")

    else:
        form = UserRegister()

    context = {
        "form": form,
    }
    return render(request, "news/register.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLogin(data=request.POST)  # для логина обязательна data=
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в аккаунт")  # сообщения
            return redirect("home")
        else:
            messages.error(request, "Неверный логин или пароль")

    else:
        form = UserLogin()

    context = {
        "form": form,
    }
    return render(request, "news/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


def feedback(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data["subject"], form.cleaned_data["content"],
                             "testsubj88@yandex.ru", ["sgrimj@gmail.com", ], fail_silently=False)
            if mail:
                messages.success(request, "Письмо отправлено")
                return redirect("feedback")
            else:
                messages.error(request, "Ошибка отправки")
        else:
            messages.error(request, "Ошибка заполнения")

    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, "news/feedback.html", context)


class HomeNews(MyMixin, ListView):  # примет на себя фунуционал index путем переопределения
    model = News  # тоже самое что и news = News.objects.all()
    template_name = "news/index.html"  # меняем дефалтный шаблон
    context_object_name = "news"  # меняем название обьекта с данными
    mixin_prop = "hello w"
    paginate_by = 4

    # queryset = News.objects.select_related("category")  тоже что и в def get_queryset(self):
    # extra_context = {
    #                 "title": "Список новостей",
    #                  }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)  # наследуем то что было
        # в родительском методе
        context["title"] = "Список новостей"  # дополняем контекст своими данными
        # context[ "mixin_prop"] = self.get_prop()  # пользуемся миксином(примесью) context["title"] = self.get_upper("Список новостей")
        return context

    def get_queryset(self):  # фильтр данных
        return News.objects.filter(is_published=True).select_related("category")
    # select_related("category") добавляет жадный запрос к бд, который грузит данные сразу 1 запросом избавляя
    # от кучи отложенных запросов потом (((для ForeignKey)))


# def index(request):    # тоже самое что и класс выше
#     news = News.objects.all()
#     context = {
#         "news": news,
#         "title": "Список новостей",
#     }
#     return render(request, "news/index.html", context)

class NewsByCategory(MyMixin, ListView):  # примет на себя фунуционал category путем переопределения
    model = News
    template_name = "news/index.html"
    context_object_name = "news"
    allow_empty = False  # уберет пустые списки и ошибку несуществующей категории
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)  # наследуем то что было
        # в родительском методе
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        # context["title"] = self.get_upper(Category.objects.get(pk=self.kwargs["category_id"]))
        return context

    def get_queryset(self):  # фильтр данных
        return News.objects.filter(category_id=self.kwargs["category_id"], is_published=True).select_related("category")


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = "news_id"
    template_name = "news/news.html"
    context_object_name = "news"
    allow_empty = False  # уберет пустые списки и ошибку несуществующей категории

    def get_queryset(self):
        return News.objects.filter(pk=self.kwargs["pk"], is_published=True)


class CreateNews(LoginRequiredMixin,
                 CreateView):  # LoginRequiredMixin для доступа только после авторизации и перенаправления на страницу авторизации
    form_class = NewsForm
    template_name = "news/add_news.html"
    # success_url = reverse_lazy("home")  # ссылка для редиректа после добавления новости
    # login_url = "/admin/" #если не авторизован то закинет по этой ссыли
    raise_exception = True


class ViewAddComments(CreateView):
    form_class = CommentsForm
    template_name = "news/comments.html"

    def get_initial(self):
        initial = super(ViewAddComments, self).get_initial()
        initial.update({"nickname": self.request.user.username})
        return initial

    def get_context_data(self, **kwargs, ):
        context = super().get_context_data(**kwargs)
        context["commentary"] = Comments.objects.all()
        context["title"] = "Комментарии"
        return context
