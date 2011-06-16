from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from models import UserProfile, UserFollow

class OpenIdMock(object):
    """ Stub the open id """
    sreg = None
    ax = None

    def get(self, *args):
        return None

class AccountsTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin',
            'admin@admin.com', 'admin')
        self.superuser.save()

        self.user = User.objects.create_user('test', 'test@email.com', 'test')
        self.user.save()

        user_profile = UserProfile(user=self.user)
        user_profile.save()

        self.client.login(username='test', password='test')

        self.user2 = User.objects.create_user('user2', 'test1@email.com',
                                              'test')
        self.user2.save()

        user_profile = UserProfile(user=self.user2)
        user_profile.save()

class TestAnonymousViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@email.com', 'test')
        self.user.save()

        user_profile = UserProfile(user=self.user)
        user_profile.save()

    def test_view_profile(self):
        res = self.client.get(reverse('accounts_user', args=['test']))
        self.assertTrue(res.status_code, 200)

    def test_change_style(self):
        """ Change pygments style for an anonymous user """

        res = self.client.get(reverse("accounts_update_field"), {
            'field':'style',
            'value': 'monokai'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, "OK")
        self.assertEqual(self.client.session['style'], u'monokai')

    def _register_mock(self):
        """ Call this to instantiate a session """
        self.client.logout()
        self.client.get('/admin/')
        session = self.client.session
        openid_mock = OpenIdMock()
        session['openid'] = openid_mock
        session.save()

    def test_register(self):
        """ Register a new user """

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'testuser',
            'email': 'some@email.com',
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(User.objects.get(username='testuser').username,
                        'testuser')

    def test_register_bad_username(self):
        """ Try to register a user with bad username """
        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'bad use r',
            'email': 'some@email.com',
        }, follow=True)
        self.assertTrue("Usernames can only contain letters, numbers and "
                        "underscores" in res.content)

    def test_register_taken_username(self):
        """ Try to register a user with 2 users with the same username"""

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'username',
            'email': 'some@email.com',
        }, follow=True)
        self.assertEqual(User.objects.get(username='username').username,
                        'username')

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'username',
            'email': 'some1@email.com',
        }, follow=True)
        self.assertTrue(u"This username is already taken. "
                         "Please choose another." in res.content)

    def test_register_bad_email(self):
        """ Try to register a user with bad e-mail """

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'username',
            'email': 'some@ ecom',
        }, follow=True)
        self.assertTrue("Enter a valid e-mail address." in res.content)

    def test_register_taken_email(self):
        """ Try to register a user with 2 users with the same e-mail"""

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'username',
            'email': 'some@email.com',
        }, follow=True)

        self._register_mock()
        res = self.client.post(reverse('user_register'), {
            'username': 'username1',
            'email': 'some@email.com',
        }, follow=True)
        self.assertTrue(u"This email is already "
        "registered in our database. Please choose another." in res.content)

class TestViews(AccountsTestCase):
    """ Test basic views methods """

    def test_view_profile(self):
        """ View a user's profile """
        res = self.client.get(reverse('accounts_profile'))
        self.assertTrue(res.status_code, 200)

    def test_profile_404(self):
        """There can be an administrator that doesn't have a profile """

        res = self.client.get(reverse('accounts_user', args=['admin']))
        self.assertTrue(res.status_code, 404)

    def test_profile_private(self):
        """ Set a profile as private and try to access it"""
        user_profile = UserProfile.objects.get(user=self.user2)
        user_profile.profile_privacy = 'private'
        user_profile.save()

        res = self.client.get(reverse('accounts_user',
                            args=[self.user2.username]))
        self.assertTrue(res.status_code, 404)

    def test_view_edit_profile(self):
        """ View edit profile form """
        res = self.client.get(reverse('accounts_edit'))
        self.assertEqual(res.status_code, 200)

    def test_edit_profile(self):
        """Submit form data"""
        res = self.client.post(reverse('accounts_edit'), {
            'email': 'test1email@email.com',
            'url': 'http://test.com/',
            'about': 'Some about text',
            'newsletter': 'checked',
            'style': 'friendly',
            'profile_privacy': 'public',
            'snippet_privacy': 'private',
        })

        user_profile = self.user.get_profile()
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, 'test1email@email.com')
        self.assertEqual(user_profile.url, 'http://test.com/')
        self.assertEqual(user_profile.about, 'Some about text')
        self.assertEqual(user_profile.newsletter, True)
        self.assertEqual(user_profile.profile_privacy, 'public')
        self.assertEqual(user_profile.snippet_privacy, 'private')

    def test_refresh_key(self):
        """Refresh REST key"""
        restkey = self.user.get_profile().restkey
        res = self.client.get(reverse('accounts_refresh_key'))
        self.assertNotEqual(restkey,
                            UserProfile.objects.get(user=self.user).restkey)

    def test_follow(self):
        """ test user follows user2 """

        self.client.get(reverse('accounts_follow', args=['user2']))
        self.assertEqual(UserFollow.objects.filter(user=self.user).filter(
                                  followed_user=self.user2).count(), 1)
        res = self.client.get(reverse('accounts_user', args=['user2']))
        self.assertTrue('1 followers' in res.content)

    def test_unfollow(self):
        """ test user unfollows user2 """
        user_follow = UserFollow(user=self.user, followed_user=self.user2)
        user_follow.save()
        res = self.client.get(reverse('accounts_unfollow', args=['user2']))
        self.assertEqual(UserFollow.objects.filter(user=self.user).filter(
                                  followed_user=self.user2).count(), 0)

    def test_followers(self):
        """ display user followers """
        user_follow = UserFollow(user=self.user, followed_user=self.user2)
        user_follow.save()
        res = self.client.get(reverse('accounts_followers', args=['user2']))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'test')

    def test_following(self):
        """ display what user is following """
        user_follow = UserFollow(user=self.user, followed_user=self.user2)
        user_follow.save()
        res = self.client.get(reverse('accounts_following', args=['test']))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'user2')

    def test_unsubscribe(self):
        """ Unsubscribe from all newsletters and notifications """
        self.client.get(reverse("accounts_refresh_key"))
        user_profile = UserProfile.objects.get(user=self.user)
        res = self.client.get(reverse('accounts_unsubscribe') + '?key=%s' %
                              user_profile.restkey, follow=True)
        #refresh
        user_profile = UserProfile.objects.get(user=self.user)
        assert user_profile.user_follows_you == False
        assert user_profile.followed_user_created == False
        assert user_profile.user_commented == False
        assert user_profile.user_shared == False
        assert user_profile.my_snippet_changed == False
        assert user_profile.newsletter == False


    def test_update_field(self):
        """ Test update some UserProfile field """

        res = self.client.get(reverse("accounts_update_field"), {
            'field':'style',
            'value': 'monokai'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, "OK")

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.style, 'monokai')

    def test_bad_update_field(self):
        res = self.client.get(reverse("accounts_update_field"), {
            'field':'user_id',
            'value':'1'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, 'ERROR: Not in allowed fields')
