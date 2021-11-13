from django.contrib import admin
from .models import Post,Tag,Comment,Category
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post,MarkdownxModelAdmin)
admin.site.register(Comment)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag,TagAdmin)
admin.site.register(Category,CategoryAdmin)
# Register your models here.
