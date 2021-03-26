from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path("feedback/", feedback, name="feedback"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    # path("", cache_page(60)(HomeNews.as_view()), name="home"),  # cache_page(60) кэш апи
    path("", HomeNews.as_view(), name="home"),
    path("category/<int:category_id>/", NewsByCategory.as_view(), name="category"),
    path("news/<int:pk>/", ViewNews.as_view(), name="news"),
    path("news/add-news/", CreateNews.as_view(), name="add_news"),
    path("news/comments/", ViewAddComments.as_view(), name="comments"),
]
