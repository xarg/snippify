from django.db import models
from django.contrib.auth.models import User
from pygments.styles import get_all_styles

ALL_STYLES = tuple([(s, s) for s in get_all_styles()])
PRIVACY_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    location = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=200, blank=True)
    about = models.CharField(max_length=500, blank=True)
    style = models.CharField(max_length=200, default="friendly",
                             choices=ALL_STYLES,
                             help_text="Default pygments style")

    """
    Private key for REST API
    """
    restkey = models.CharField(max_length=40)

    """ E-mail notifications """
    user_follows_you = models.BooleanField(default=True,
                                           verbose_name="Users follows me",
                                           help_text="Notify me when someone"
                                           "starts following me")
    followed_user_created = models.BooleanField(default=True,
                    verbose_name="Followed user submited snippet",
                    help_text="Notify me when someone that I follow submits "
                                "a snippet")
    user_commented = models.BooleanField(default=True,
                    verbose_name='Snippet commented',
                    help_text="Notify me when I recieve a comment")
    user_shared = models.BooleanField(default=True,
                                help_text='A user shared with you a snippet')
    my_snippet_changed = models.BooleanField(default=True,
                help_text='Your snippet was changed by someone else than you')

    newsletter = models.BooleanField(default=True,
                                     help_text="I promise not to spam you")

    """ Privacy settings """
    profile_privacy = models.CharField(max_length=50, default='public',
                                       choices=PRIVACY_CHOICES)
    snippet_privacy = models.CharField(max_length=50, default='public',
                                       choices=PRIVACY_CHOICES,
                                       help_text="This is the default privacy"
                                        " setting when you add new snippets")

class UserFollow(models.Model):
    """A user can follow a User"""

    user = models.ForeignKey(User, related_name='stalkers')
    followed_user = models.ForeignKey(User, related_name='victims')
