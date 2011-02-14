""" Accounts views """
import time
import random
import hashlib

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string

from django_emailqueue.models import EmailQueue
from django_authopenid.signals import oid_register

from snippify.snippets.models import Snippet
from snippify.utils import build_context

from models import UserProfile, UserFollow
from forms import ProfileForm

def register_account(form, _openid):
    """ create an account """
    user_ob = User.objects.create_user(form.cleaned_data['username'],
                            form.cleaned_data['email'])
    user_ob.save()
    profile = UserProfile(
        user=user,
        location=form.cleaned_data['location'],
        url=form.cleaned_data['url'],
        about=form.cleaned_data['about'],
        restkey=hashlib.sha1("%s%s%s" % (str(random.random()), 'snippify.me',
                                         str(time.time()))).hexdigest(),
    )
    profile.save()
    user_ob.backend = "django.contrib.auth.backends.ModelBackend"
    oid_register.send(sender=user, openid=_openid)
    return user

@login_required
def view_profile(request, username=None):
    """ Display profile info, such as snippets, tags, and followed users """

    if username is None or username == request.user.username:
        user = request.user
        my_profile = True
    else:
        user = get_object_or_404(User, username=username)
        my_profile = False

    try:
        user_profile = UserProfile.objects.filter(user=user).get()
    except UserProfile.DoesNotExist:
        raise Http404

    if user != request.user and user_profile.profile_privacy == 'private':
        raise Http404
    try:
        UserFollow.objects.filter(user=request.user,
                                  followed_user=user).get()
        is_following = True
    except:
        is_following = False


    snippets = Snippet.objects.filter(author=user)
    paginator = Paginator(snippets, 25)
    page = request.GET.get('page', '1')

    tags = []
    for snippet in snippets.all():
        for tag in snippet.tags.all():
            if tag not in tags:
                tags.append(tag)

    followed_users = UserFollow.objects.select_related().filter(
        user=user).all()[:14]

    followers_list = UserFollow.objects.select_related().filter(
        followed_user=user).all()[:14]

    return render_to_response(
        'accounts/profile.html', {
            'userdata': user,
            'profile': user_profile,
            'tags': tags,
            'snippets': paginator.page(page).object_list,
            'followed_users': followed_users,
            'followers': followers_list,
            'is_following': is_following,
            'sidebared': True,
            'my_profile': my_profile,
        },
        context_instance=build_context(request)
    )

@login_required
def edit(request):
    """ Update UserProfile """

    if request.method == 'POST':
        form = ProfileForm(request.POST,
                           instance=UserProfile.objects.get(user=request.user))
        if form.is_valid(): # All validation rules pass
            try:
                User.objects.filter(email=form.cleaned_data['email']).\
                exclude(pk=request.user.pk).get()
                request.session['flash'] = ['This e-mail is already in use',
                                            'error']
                return HttpResponseRedirect(
                    request.META.get('HTTP_REFERER', '/'))
            except User.DoesNotExist:#Check if the e-mail is not already in use
                pass
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            request.session['flash'] = ['Your profile has been updated',
                                        'success']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ProfileForm(instance=UserProfile.objects.get(user=request.user),
                           initial = {'email': request.user.email})
    return render_to_response('accounts/edit.html', {'form': form},
                              context_instance=build_context(request))

@login_required
def refresh_key(request):
    """ Regenerate private REST key """
    profile = UserProfile.objects.get(user=request.user)
    profile.restkey = hashlib.sha1(str(random.random()) +
                                   'snippify.me' +
                                   str(time.time())).hexdigest()
    profile.save()
    request.session['flash'] = ['Your private key has been refreshed, now '
                                'update it in your plugin settings', 'success']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def follow(request, follow_username = None):
    """ Follow a User """
    try:
        follow_user = User.objects.get(username = follow_username)
        followed_item = UserFollow()
        followed_item.user = request.user
        followed_item.followed_user = follow_user
        followed_item.save()
        try:
            profile = UserProfile.objects.get(user=follow_user)
            if profile.user_follows_you: #User wants to recieve a notification
                queue = EmailQueue(
                    mail_to=follow_user.email,
                    mail_subject="User started following you",
                    mail_body=render_to_string('emails/user_follows_you.txt', {
                        'user': follow_user,
                        'username_that_follows': request.user.username,
                        'SITE': request.META['HTTP_HOST']}
                    )
                )
                queue.save()
        except:
            pass
        request.session['flash'] = ['You started following %s' %
                                    follow_user.username, 'success']
    except:
        request.session['flash'] = ['This user does not exist', 'error']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def unfollow(request, follow_username = None):
    """ Stop following a user """
    try:
        follow_user = User.objects.get(username = follow_username)
        followed_item = UserFollow.objects.get(user = request.user,
                                               followed_user = follow_user)
        followed_item.delete()
        request.session['flash'] = ['You stoped following %s' %
                                    follow_user.username, 'success']
    except:
        request.session['flash'] = ['This user does not exist', 'error']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def followers(request, username = None):
    """ Who are your followers Jesus? """
    data = {}
    data['userdata'] = get_object_or_404(User, username=username)
    data['attribute'] = 'user'
    try:
        data['users'] = UserFollow.objects.select_related().filter(
            followed_user=data['userdata']).all()
    except:
        data['users'] = None
    return render_to_response('accounts/followers.html', data,
                              context_instance=build_context(request))

def following(request, username= None):
    """ Who is following username """
    data = {}
    data['userdata'] = get_object_or_404(User, username=username)
    data['attribute'] = 'followed_user'
    try:
        data['users'] = UserFollow.objects.select_related().filter(
            user=data['userdata']).all()
    except:
        data['users'] = None
    return render_to_response('accounts/following.html', data,
                              context_instance=build_context(request))

def unsubscribe(request):
    """ Unsubscribe from all notifications and newsletter """

    key = request.GET.get('key', None)
    if key:
        try:
            profile = UserProfile.objects.get(restkey = key)
            profile.user_follows_you = False
            profile.followed_user_created = False
            profile.user_commented = False
            profile.user_shared = False
            profile.my_snippet_changed = False
            profile.newsletter = False
            profile.save()
            request.session['flash'] = ['You have been unsubscribed from all '
                                        'emails', 'success']
        except UserProfile.DoesNotExist:
            request.session['flash'] = ['The key is not correct. Contact the '
                                        'administrator.', 'error']
    return HttpResponseRedirect('/')
