import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def snippify(value):
    """
    Searches for all #(\d+) and replaces URL /\1
    """
    value = re.sub(r"#(\d+)", r"<a class='snippet-url' href='/\1'>#\1</a>",
                   value)
    return re.sub(r"@(\w+)", r"<a class='user-url' href='/accounts/\1'>@\1</a>",
                  value)
