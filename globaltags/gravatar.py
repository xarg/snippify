import hashlib
from django import template

register = template.Library()

@register.simple_tag
def gravatar(email, size=48):
    """
    Simply gets the Gravatar for the commenter. There is no rating or
    custom "not found" icon yet. Used with the Django comments.
    
    If no size is given, the default is 48 pixels by 48 pixels.
    
    Template Syntax::
    
        {% gravatar comment.user_email [size] %}
        
    Example usage::
        
        {% gravatar comment.user_email 48 %}
    
    """
    
    hash = hashlib.md5(email).hexdigest()
    return """<img src="http://www.gravatar.com/avatar/%s?s=%s" width="%s" height="%s" alt="gravatar" class="gravatar" />""" % (hash, size, size, size)