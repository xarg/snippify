from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from models import UserProfile, UserFollow

class AccountsTestCase(TestCase):
    def setUp(self):
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

class TestViews(AccountsTestCase):
    """ Test basic views methods """

    def test_view_profile(self):
        res = self.client.get(reverse('accounts_profile'))
        self.assertTrue(res.status_code, 200)

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

        res = self.client.get(reverse('accounts_follow', args=['user2']))
        self.assertEqual(UserFollow.objects.filter(user=self.user).filter(
                                  followed_user=self.user2).count(), 1)

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
