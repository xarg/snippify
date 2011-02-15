# -*- coding: utf-8 -*-
import datetime

from haystack import site, fields
from haystack.indexes import SearchIndex

from models import Snippet

class SnippetIndexer(SearchIndex):
    """ Haystack indexer """
    text = fields.CharField(document=True, use_template=True)
    created_date = fields.DateField(model_attr='created_date')
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Snippet.objects.filter(
            created_date__lte=datetime.datetime.now())

site.register(Snippet, SnippetIndexer)
