from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect
from users.models import UserProfile
from utils import response, post_data
from users.decorators import anonymoususer
from django.shortcuts import get_object_or_404

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

@anonymoususer
def view_register(request, registration_template, next=''):
    from users.forms import RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(post_data(request))
        if form.is_valid():
            userprofile = _handle_user_registration(form)
            return _let_user_login(request,
                                   userprofile.user,
                                   email=form.cleaned_data.get('email'),
                                   password=form.cleaned_data.get('password'),
                                   next=form.cleaned_data.get('next'))
    else:
        form = RegistrationForm()
    return response(request, registration_template, {'form': form, 'next': next})

def _handle_user_registration(registration_form):
    userprofile = UserProfile.objects.create_userprofile(email=registration_form.cleaned_data.get('email'),
                                           password=registration_form.cleaned_data.get('password'),
                                           name=registration_form.cleaned_data.get('name'))
    return userprofile

def _authenticate_user(user):
    raise NotImplementedError

def _let_user_login(request, user, email, password, next=''):
    user = django_authenticate(username=email, password=password)
    django_login(request, user)
    if next:
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_homepage'))

@anonymoususer
def view_login(request, login_template, next=''):
    from users.forms import LoginForm
    if request.method == 'POST':
        form = LoginForm(post_data(request))
        if form.is_valid():
            userprofile = UserProfile.objects.get(email=form.cleaned_data.get('email'))
            return _let_user_login(request,
                                   userprofile.user,
                                   email=form.cleaned_data.get('email'),
                                   password=form.cleaned_data.get('password'),
                                   next=form.cleaned_data.get('next'))
    else:
        form = LoginForm()
    return response(request, login_template, {'form': form, 'next': next})

def view_logout(request, logout_template):
    django_logout(request)
    return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_homepage'))

def view_userprofile(request, user_id, user_slug_name, userprofile_template):
    userprofile = get_object_or_404(UserProfile, id=int(user_id), slug=user_slug_name)
    submitted_snippets = [{'title': snippet.title,
                           'slug': snippet.slug,
                           'id': snippet.id,
                           'active': snippet.active} for snippet in userprofile.submitted_snippets()]
    return response(request, userprofile_template, {'userprofile': userprofile,
                                                    'submitted_snippets': submitted_snippets})
