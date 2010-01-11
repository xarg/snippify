from django import forms
from snippify.snippets.models import Snippet

class SnippetForm(forms.ModelForm):
    body = forms.Textarea(attrs={'class':'special', 'wrap': 'off'})
    class Meta:
        model = Snippet
        exclude = ('author','created_date', 'updated_date', 'via')
