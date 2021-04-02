from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
from testapp.models import Rubric, Article


# from mptt.admin import MPTTModelAdmin
# class CustomMPTTModelAdmin(MPTTModelAdmin):
#     # specify pixel amount for this ModelAdmin only:
#     mptt_level_indent = 20  # отступы для дерева в админке
#
# admin.site.register(Rubric,CustomMPTTModelAdmin )
admin.site.register(
    Rubric,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.register(Article)