from django.contrib import admin
from snippify.snippets.models import Snippet, SnippetComment, SnippetVersion

class SnippetAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'lexer', 'created_date', 'author')
    list_filter = ('lexer', 'author', )
    search_fields = ('title', 'body', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

class SnippetCommentAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'user', 'created_date', )

class SnippetVersionAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'version', 'created_date', )

admin.site.register(Snippet, SnippetAdmin)
admin.site.register(SnippetComment, SnippetCommentAdmin)
admin.site.register(SnippetVersion, SnippetVersionAdmin)
