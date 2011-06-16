import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from snippify.utils import order_fields
from models import UserProfile

class ProfileForm(forms.ModelForm):
    """ Profile edit form """

    email = forms.EmailField()

    def __init__(self, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        self.fields = order_fields(self.fields, ['email'])

    class Meta:
        model = UserProfile
        exclude = ['user', 'user_shared', 'my_snippet_changed', 'restkey']

attrs_dict = { 'class': 'login'}
username_re = re.compile(r'^\w+$')

class OpenidRegisterForm(forms.Form):
    """ openid signin form """
    username = forms.CharField(max_length=30,
            widget=forms.widgets.TextInput(attrs=attrs_dict))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
        maxlength=200)), label=u'Email address')
    url = forms.URLField(max_length=200, required = False,
            widget=forms.widgets.TextInput(attrs=attrs_dict))
    location = forms.CharField(max_length=50, required = False,
            widget=forms.widgets.TextInput(attrs=attrs_dict),
            help_text=u'Ex. Moscow, RU')
    about = forms.CharField(max_length=500, required = False,
            widget=forms.widgets.Textarea(attrs=attrs_dict))

    def __init__(self, *args, **kwargs):
        super(OpenidRegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean_username(self):
        """ test if username is valid and exist in database """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(_(u"Usernames can only contain "
                                           "letters, numbers and underscores"))
            try:
                User.objects.get(username__exact =\
                        self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
            raise forms.ValidationError(_(u"This username is already taken. "
                                            "Please choose another."))

    def clean_email(self):
        """For security reason one unique email in database"""
        if 'email' in self.cleaned_data:
            try:
                User.objects.get(email = self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            raise forms.ValidationError(_(u"This email is already "
                "registered in our database. Please choose another."))

