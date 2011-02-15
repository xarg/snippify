from django.contrib import admin
from snippify.snippets.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    exclude = ('author','updated_date')
    list_display = ('title', 'lexer', 'created_date', 'author')
    list_filter = ('lexer', 'author', )
    search_fields = ('title', 'body', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Snippet, SnippetAdmin)
