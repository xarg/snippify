# -*- coding: utf-8 -*-
"""Functional tests"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
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
        """ """

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

class PistonTests(SnippetsTestCase):
    """ REST Tests """
