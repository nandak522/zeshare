from quest.models import Snippet
from django.shortcuts import get_object_or_404
from utils import response

def is_snippetowner(the_function):
    def _is_snippetowner(request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=int(kwargs.get('snippet_id')))
        user = request.user
        if snippet.owner == user.get_profile():
            return the_function(request, *args, **kwargs)
        message = 'You dont have permissions to modify this snippet'
        return response(request, kwargs.get('snippet_profile_template'),
                        {'snippet': snippet,
                         'owner': False,
                         'message': message})
    return _is_snippetowner