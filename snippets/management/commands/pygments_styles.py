# -*- coding: utf-8 -*-
""" Regenerate all pygments styles for html format and put them in the
    MEDIA_ROOT/css/pygments/

"""
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

class Command(BaseCommand):

    def handle(self, *args, **options):
        style_dir = os.path.join(settings.MEDIA_ROOT, 'css', 'pygments')

        for style in get_all_styles():
            formatter = HtmlFormatter(style=style)
            css = formatter.get_style_defs()
            with open(os.path.join(style_dir, style + '.css'), 'w') as f:
                f.write(css)
