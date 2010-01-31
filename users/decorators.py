from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect
from utils import get_data

def anonymoususer(the_function):
    def _anonymoususer(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_homepage'))
        kwargs['next'] = get_data(request).get('next', '')
        return the_function(request, *args, **kwargs)
    return _anonymoususer