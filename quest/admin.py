from quest.models import Snippet
from django.contrib import admin

class SnippetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}
    list_display = ('title', 'public', 'active')
    search_fields = ('title', 'slug')
    list_filter = ('public', 'active')
    list_per_page = 25
    
admin.site.register(Snippet, SnippetAdmin)