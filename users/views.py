from django.contrib.auth import logout
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect
from users.models import UserProfile
from utils import response
    
def view_all_users(request, all_users_template):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(UserProfile.objects.values('id', 'name', 'email', 'slug'), 2)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)
    return response(request, all_users_template, {'users': users})

def view_login(request, login_template):
    raise NotImplementedError

def view_logout(request, logout_template):
    logout(request)
    return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_homepage'))

def view_userprofile(request, user_id, user_slug_name, userprofile_template):
    raise NotImplementedError