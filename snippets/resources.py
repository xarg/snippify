from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication

from models import Snippet
from snippify.accounts.models import UserProfile
#from forms import SnippetCreateForm

#FIELDS = ('author', 'title', 'description', 'body', 'lexer', 'tags', )

class RestKeyAuthentication(ApiKeyAuthentication):
    """ Authorize users based on their restkey """

    def is_authenticated(self, request, **kwargs):
        api_key = request.GET.get('api_key') or request.POST.get('api_key')

        if not api_key:
            return self._unauthorized()
        try:
            profile = UserProfile.objects.get(restkey=api_key)
            request.user = profile.user
        except UserProfile.DoesNotExist:
            return self._unauthorized()
        return True

class SnippetResource(ModelResource):
    """ Snippet rest stuff """

    class Meta:
        queryset = Snippet.objects.filter(privacy=u'public')
        authentication = RestKeyAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['updated_date', 'via', 'privacy', 'status', ]
        filtering = {
            'id': ALL,
            'author': ALL_WITH_RELATIONS,
            'created_date': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
