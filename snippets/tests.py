# -*- coding: utf-8 -*-
"""Functional tests"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from snippify.accounts.models import UserProfile
from django_emailqueue.models import EmailQueue

from models import Snippet, SnippetComment

import json

class SnippetsTestCase(TestCase):
    def setUp(self):
        """ Create a user, superuser and few snippets """
        self.user = User.objects.create_user('user', 'user@email.com',
                                             'password')
        user_profile = UserProfile(user=self.user, restkey='key')
        user_profile.save()

        self.superuser = User.objects.create_superuser('superuser',
                                                       'superuser@email.com',
                                                       'password')

        self.client.login(username='user', password='password')

        self.snippet_text = Snippet.objects.create(
            author=self.user,
            title="Text file",
            description="Text file for testing",
            lexer="txt",
            body="""This is a text snippet
            this is is the second line
            """
        )

        self.snippet_python = Snippet.objects.create(
            author=self.user,
            title="Python snippet",
            description="Python snippet for testing",
            lexer="python",
            body="""Snippet body""",
        )
        self.snippet_python.tags.add("python", "code")

class SnippetsViewsTests(SnippetsTestCase):
    """ Snippets views tests """

    def test_add_snippet(self):
        """Using the snippets_create view add a snippet"""
        response = self.client.get(reverse('snippets_create'))
        self.assertEqual(response.status_code, 200)

        data = {
            'title': 'Snippet 3',
            'description': 'Snippet 3 4',
            'body': """#!/usr/bin/python
x=3
""",
            'tags': 'python test-tag'
        }

        #First one is search
        response = self.client.post(reverse('snippets_create'), data)

        self.assertEqual(response.status_code, 302)
        snippet = Snippet.objects.get(title="Snippet 3")
        #Pygments guessed the correct lexer
        self.assertEqual('Snippet 3', str(snippet))
        for field, value in data.items():
            if field == 'tags':
                self.assertEqual([t.name for t in snippet.tags.all()],
                                 data['tags'].split(" "))
            else:
                self.assertEqual(getattr(snippet, field), value)

    def test_update_snippet(self):
        """ """
        title_text = "Updated title"
        response = self.client.post(
            reverse('snippets_update', None, [self.snippet_text.pk]), {
                "title": title_text,
                "description": self.snippet_text.description,
                "body": self.snippet_text.body,
                'status': 'published',
                'privacy': 'public',
            })
        self.assertEqual(response.status_code, 302)
        updated_snippet = Snippet.objects.get(pk=self.snippet_text.pk)
        self.assertEqual(updated_snippet.title, title_text)

    def test_preview_snippet(self):
        """ When the user click the preview button an ajax request will be called
        which returns a html content of the snippet"""

        response = self.client.post(
            reverse('snippets_preview', None, []), {
                "body": self.snippet_text.body,
                'lexer': u'text',
                'style': u'friendly',
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('This is a text snippet' in response.content)

    def test_history(self):
        """Check snippet versions"""

    def test_search(self):
        """ Test the search results """

    def test_suggest(self):
        """Test autosuggest (used in firefox search plugin and google chrome)"""

    def test_download(self):
        """Downloading snippet"""

    def test_delete(self):
        """Make sure it redirects properly"""

class CommentsTestCase(SnippetsTestCase):
    """ Testing comments functionality """

    def test_create(self):
        """ Comment on a specific snippet """

        body = u'this is a comment'
        response = self.client.post(reverse('snippets_comment', None, [1]), {
            'body': body
        })
        self.assertEqual(SnippetComment.objects.get(snippet=1).body, body)
        self.assertTrue(body in json.loads(response.content)['content'])

    def test_create_no_body(self):
        """ """
        response = self.client.post(reverse('snippets_comment', None, [1]))
        self.assertEqual(len(SnippetComment.objects.all()), 0)
        self.assertTrue('Body field is required' in response.content)

    def test_create_notification(self):
        """ If an user comments on another user's snippets then an notification
        should be sent.

        """
        self.client.login(username='superuser', password='password')
        self.test_create()
        self.assertEqual(len(EmailQueue.objects.all()), 1)

    def test_create_no_anonymous(self):
        """ Anonymous users can't post comments """

        self.client.logout()
        response = self.client.post(reverse('snippets_comment', None, [1],),
            {'body': 'a body'})
        self.assertEqual(len(SnippetComment.objects.all()), 0)
        self.assertEqual(u'You must login to post a comment',
                         json.loads(response.content)['error'])

    def test_delete(self):
        """ Administrators should be able to delete comments """
        self.test_create()
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('snippets_comment',
                        args=[1],) + '?delete=1', follow=True)
        self.assertEqual(len(SnippetComment.objects.all()), 0)
        self.assertTrue('Comment deleted succesfully' in response.content)

    def test_delete_fail(self):
        """ Users should NOT be able to delete comments """
        self.test_create()
        response = self.client.get(reverse('snippets_comment',
                        args=[1],) + '?delete=1', follow=True)
        self.assertEqual(len(SnippetComment.objects.all()), 1)
        self.assertTrue('Permission denied' in response.content)


class TagTests(SnippetsTestCase):
    """Test tag views"""

    def test_tags_index(self):
        """All the tags"""

    def test_tag(self):
        """All the snippets in one tag"""

    def test_tag_user(self):
        """All user's snippets tagged with a specific tag"""

class ApiTests(SnippetsTestCase):

    def test_create(self):
        """" """
