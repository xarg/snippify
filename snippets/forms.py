from django import forms
from snippify.snippets.models import Snippet

class SnippetUpdateForm(forms.ModelForm):
    body = forms.Textarea(attrs={'class':'special', 'wrap': 'off'})
    description = forms.CharField(widget=forms.widgets.Textarea(
                                        attrs={'rows': 5}))
    class Meta:
        model = Snippet
        exclude = ('author', 'via')

class SnippetCreateForm(forms.ModelForm):
    body = forms.Textarea(attrs={'class':'special', 'wrap': 'off'})
    description = forms.CharField(widget=forms.widgets.Textarea(
                                        attrs={'rows': 5}))
    class Meta:
        model = Snippet
        exclude = ('author', 'via', 'status', 'privacy')
