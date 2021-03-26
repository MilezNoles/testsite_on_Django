from django import template
from news.models import Category
from django.db.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(news__is_published__contains=True).annotate(cnt=Count("news")).filter(cnt__gt=0)




@register.inclusion_tag("news/list_categories.html")
def show_cat():
    categories = cache.get("categories",)             # обращаемся в кэш, если там нет ничего то заполняем на 500сек
    if not categories:
        categories = Category.objects.annotate(cnt=Count("news", filter=F("news__is_published"))).filter(cnt__gt=0)
        cache.set("categories", categories, 500)
    return {"categories": categories,}