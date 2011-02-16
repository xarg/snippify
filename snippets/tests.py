# -*- coding: utf-8 -*-
"""Functional tests"""
import lxml.html

from django.test import TestCase
from django.core.urlresolvers import reverse
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

    def test_basic_snippet(self):
        """ Add, update, remove, test if pygments is working

        XXX: Split this into multiple tests

        """

        #Add
        response = self.client.get(reverse('snippify_create'))
        self.assertEqual(response.status_code, 200)
        #First one is search
        form = lxml.html.document_fromstring(response.content).forms[1]
        response = self.client.post(reverse('snippify_create'), {
            'csrfmiddlewaretoken': form.fields['csrfmiddlewaretoken'],
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
        self.assertEqual('Snippet 3 (python)', str(snippet))

        #Update
        response = self.client.get(reverse('snippify_update', None,
                                           [snippet.id]))
        self.assertEqual(response.status_code, 200)
        form = lxml.html.document_fromstring(response.content).forms[1]

    def test_add_snippet(self):
        """ """

    def test_update_snippet(self):
        """ """

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


class TagTests(SnippetsTestCase)
