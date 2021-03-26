from django.db import models
from django.urls import reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")  # обязательный атрибут - длина
    content = RichTextUploadingField(blank=True, verbose_name="контент")  # по умолчанию пустой
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")  # про создании новости
    # поставится не изменяемая дата и время,которые будут взяты в момент создания
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Обновлено")  # меняет дату и время с каждым изменением
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name="Фото", blank=True)
    # фото будут сохраняться в папке фото/год.месяц.день
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано?")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория", )
    views = models.IntegerField(default=0)

    def get_absolute_url(self):   # для ссылок
        return reverse_lazy("news", kwargs={"pk": self.pk, })

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"  # имя в админке ед число
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]  # + , "title"


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Наименование категории")

    def get_absolute_url(self):
        return reverse_lazy("category", kwargs={"category_id": self.pk, })

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["pk"]


class Comments(models.Model):
    nickname = models.CharField(max_length=50, verbose_name="Имя пользователя", )  # обязательный атрибут - длина
    message = RichTextUploadingField(verbose_name="Комментарий")  # по умолчанию пустой
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")  # про создании новости
    # поставится не изменяемая дата и время,которые будут взяты в момент создания
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Обновлено")  # меняет дату и время с каждым изменением
    avatar = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name="Фото", blank=True)
    # фото будут сохраняться в папке фото/год.месяц.день

    def get_absolute_url(self):  # для ссылок
        return reverse_lazy("comments")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Комментарий"  # имя в админке ед число
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]
