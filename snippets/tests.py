# -*- coding: utf-8 -*-
"""Functional tests"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from snippify.accounts.models import UserProfile

from models import Snippet, SnippetComment, SnippetVersion

class SnippetsTestCase(TestCase):
    def setUp(self):
        """ Create a user, superuser and few snippets """
        self.user = User.objects.create_user('user', 'user@email.com',
                                             'password')
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

    def test_comment_snippet(self):
        """ Comment on a specific snippet """

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

class TagTests(SnippetsTestCase):
    """Test tag views"""

    def test_tags_index(self):
        """All the tags"""

    def test_tag(self):
        """All the snippets in one tag"""

    def test_tag_user(self):
        """All user's snippets tagged with a specific tag"""

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user('test', 'test@email.com', 'test')
        self.user.save()

        user_profile = UserProfile(user=self.user, restkey='key')
        user_profile.save()

    def test_create(self):
        self.client.get(reverse('api_create_snippet'), HTTP_RESTKEY='key')
        import pdb; pdb.set_trace()
