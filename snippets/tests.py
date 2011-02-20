# -*- coding: utf-8 -*-
"""Functional tests"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Snippet, SnippetComment, SnippetVersion

class SnippetsTestCase(TestCase):
    def setUp(self):
        """ Load fixtures and stuff """
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
            body="""Snippet body"""
        )

class SnippetsViewsTests(SnippetsTestCase):
    """ Snippets views tests """

    def test_add_snippet(self):
        """ """
        response = self.client.get(reverse('snippets_create'))
        self.assertEqual(response.status_code, 200)

        #First one is search
        response = self.client.post(reverse('snippets_create'), {
            'title': 'Snippet 3',
            'description': 'Snippet 3 4',
            'body': """#!/usr/bin/python
x=3
""",
            'status': 'published',
            'privacy': 'public',
            'tags': 'text'
        })

        self.assertEqual(response.status_code, 302)
        snippet = Snippet.objects.get(title="Snippet 3")
        #Pygments guessed the correct lexer
        self.assertEqual('Snippet 3', str(snippet))

    def test_update_snippet(self):
        """ """
        title_text = "Update title"
        response = self.client.post(
            reverse('snippets_update', None, [self.snippet_text.pk]), {
                "title": title_text,
                "description": self.snippet_text.description,
                "body": self.snippet_text.body,
                'status': 'published',
                'privacy': 'public',
                'tags': 'text'
            })
        updated_snippet = Snippet.objects.get(pk=self.snippet_text.pk)
        self.assertEqual(updated_snippet.title, title_text)

    def test_preview_add_snippet(self):
        """ """

    def test_preview_update_snippet(self):
        """ """

    def test_comment_snippet(self):
        """ Comment on a specific snippet """

    def test_history(self):
        """ Check history functionality """

    def test_search(self):
        """ Test the search results """

    def test_suggest(self):
        """ Test autosuggest """

    def test_download(self):
        """ Downloading snippet """

class PistonTests(SnippetsTestCase):
    """ REST Tests """


class TagTests(SnippetsTestCase):
    """ Test tags """
