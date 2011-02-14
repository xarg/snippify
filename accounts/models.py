from django.db import models
from django.contrib.auth.models import User

PRIVACY_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    about = models.CharField(max_length=500)

    """
    Private key for REST API
    """
    restkey = models.CharField(max_length=40)

    """ E-mail notifications """
    user_follows_you = models.BooleanField(default=True,
                                      help_text='A user started following you')
    followed_user_created = models.BooleanField(default=True,
                        help_text='A user that you follow submited a snippet')
    user_commented = models.BooleanField(default=True,
                    help_text='A user has commented on your snippet')
    user_shared = models.BooleanField(default=True,
                                help_text='A user shared with you a snippet')
    my_snippet_changed = models.BooleanField(default=True,
                help_text='Your snippet was changed by someone else than you')

    """ Privacy settings """
    profile_privacy = models.CharField(max_length=50, default='public',
                                       choices=PRIVACY_CHOICES)
    snippet_privacy = models.CharField(max_length=50, default='public',
                                       choices=PRIVACY_CHOICES)
    newsletter = models.BooleanField(default=True)

class UserFollow(models.Model):
    """ A user can follow a User or Tag """
    user = models.ForeignKey(User, related_name='stalkers')
    followed_user = models.ForeignKey(User, related_name='victims')
