from django.contrib import admin
from .models import Post,Tag
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post,MarkdownxModelAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Tag,TagAdmin)
# Register your models here.

