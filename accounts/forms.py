import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from snippify.utils import order_fields
from models import PRIVACY_CHOICES, UserProfile

class ProfileForm(forms.ModelForm):
    """ Profile edit form """

    email = forms.EmailField()
    location = forms.CharField(required=False, max_length=50)
    url = forms.URLField(required=False, max_length=200)
    about = forms.CharField(required=False, max_length=500)

    """ E-mail notifications """
    user_follows_you = forms.BooleanField(required=False,
                                          label="Users follows me",
                                          help_text="Notify me when someone"
                                          "starts following me")
    followed_user_created = forms.BooleanField(required=False,
                                               label="Followed user submited "
                                               "snippet",
                                               help_text="Notify me when "
                                               "someone that I follow submits "
                                               "a snippet")
    user_commented = forms.BooleanField(required=False,
                                        label='Snippet commented',
                                        help_text="Notify me when I recieve a "
                                        "comment")

    """
    user_shared = forms.BooleanField(required=False, label="User shared",
                    help_text='Notify me if a user shared with me a snippet')
    my_snippet_changed = forms.BooleanField(required=False,
            help_text='Notify me if one of my snippets was changed by someone')

    """

    """ Newsletter """
    newsletter = forms.BooleanField(required=False,
                                    help_text="I promise not to spam you")
    """ Privacy settings """
    profile_privacy = forms.ChoiceField(choices=PRIVACY_CHOICES)
    snippet_privacy = forms.ChoiceField(choices=PRIVACY_CHOICES,
                                        help_text="This is the default privacy"
                                        " setting when you add new snippets")
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
                raise forms.ValidationError(_("Usernames can only contain \
                    letters, numbers and underscores"))
            try:
                user = User.objects.get(
                        username__exact = self.cleaned_data['username']
                )
            except User.DoesNotExist:
                return self.cleaned_data['username']
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'There is already more than one \
                    account registered with that username. Please try \
                    another.')
            self.user = user
            raise forms.ValidationError(_("This username is already \
                taken. Please choose another."))

    def clean_email(self):
        """For security reason one unique email in database"""
        if 'email' in self.cleaned_data:
            try:
                user = User.objects.get(email = self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'There is already more than one \
                    account registered with that e-mail address. Please try \
                    another.')
            raise forms.ValidationError(_("This email is already \
                registered in our database. Please choose another."))
