from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms
from .models import News, Category, Comments
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
    "id", "title", "category", "created_at", "updated_at", "is_published", "get_photo")  # столбцы в админке
    list_display_links = ("id", "title")  # что будет ссылкой на редактирование в админке
    search_fields = ("title", "content")  # search in admin
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")
    fields = ("title", "content", "photo", "get_photo", "is_published", "views", "created_at",
              "updated_at")  # список полей для вывода внутри новости в админке
    readonly_fields = ("get_photo", "views", "created_at", "updated_at")  # поля которые будут только для чтения
    save_on_top = True  # кнопки сохранить будут и вверху

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50'>")  # убирает экранирование
        else:
            return "Фото нету"

    get_photo.short_description = "Миниатюра"  # Меняем вывод Getphoto в столбце админки на Миниатюра


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname")
    list_display_links = ("id", "nickname")
    search_fields = ("nickname",)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)

admin.site.site_title = "Управление новостями"  # переопределение html админки
admin.site.site_header = "Управление новостями"
