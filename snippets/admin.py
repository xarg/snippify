from django.contrib import admin
from snippify.snippets.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    exclude = ('author','updated_date')
    list_diplay = ('title', 'created_date', 'author')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()        
admin.site.register(Snippet, SnippetAdmin)