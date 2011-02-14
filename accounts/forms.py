class EditForm(forms.Form):
    email = forms.EmailField()
    location = forms.CharField(required = False, max_length=50)
    url = forms.CharField(required = False, max_length=200)
    about = forms.CharField(required = False, max_length=500)
    """ E-mail notifications """
    user_follows_you = forms.BooleanField(required = False, label="Users follows me", help_text="Notify me when someone starts following me")
    followed_user_created = forms.BooleanField(required = False, label="Followed user submited snippet", help_text="Notify me when someone that I follow submits a snippet")
    user_commented = forms.BooleanField(required = False, label='Snippet commented', help_text="Notify me when I recieve a comment")
    """
    I'll implement this later
    """
    #user_shared = forms.BooleanField(required = False, label="User shared", help_text='Notify me if a user shared with me a snippet')
    #my_snippet_changed = forms.BooleanField(required = False, help_text='Notify me if one of my snippets was changed by someone')
    """ Newsletter """
    newsletter = forms.BooleanField(required = False, help_text='I promise not to spam you')
    """ Privacy settings """
    profile_privacy = forms.ChoiceField(choices = (('public', 'Public'), ('private', 'Private')))
    snippet_privacy = forms.ChoiceField(choices = (('public', 'Public'), ('private', 'Private')), help_text = "This is the default privacy setting when you add new snippets")
