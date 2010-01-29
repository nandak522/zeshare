from quest.models import Snippet
from utils import response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from quest.decorators import is_snippetowner

def view_homepage(request, homepage_template):
    return response(request, homepage_template, locals())

def view_all_snippets(request, all_snippets_template):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(Snippet.publicsnippets.values('id', 'title', 'active', 'slug'), 2)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        snippets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        snippets = paginator.page(paginator.num_pages)
    return response(request, all_snippets_template, {'snippets': snippets})

def view_snippet_profile(request, snippet_id, snippet_slug, snippet_profile_template):
    snippet = get_object_or_404(Snippet, id=int(snippet_id), slug=snippet_slug)
    user = request.user
    owner = False
    if user.is_authenticated() and snippet.owner == user.get_profile():
        owner = True
    return response(request, snippet_profile_template, {'snippet': snippet,
                                                        'owner': owner})

def view_recent_snippets(request, recent_snippets_template):
    raise NotImplementedError

def view_popular_snippets(request, popular_snippets_template):
    raise NotImplementedError

def view_add_snippet(request, add_snippet_template, snippet_profile_template):
    from quest.forms import AddSnippetForm
    if request.method == 'POST':
        form = AddSnippetForm(request.POST.copy())
        if form.is_valid():
            snippet = _handle_snippet_creation(form)
            user = request.user
            if user.is_authenticated():
                userprofile = user.get_profile()
                from quest.models import UserProfileSnippetMembership
                UserProfileSnippetMembership.objects.create_membership(userprofile=userprofile,
                                                                       snippet=snippet)
            return response(request, snippet_profile_template, {'form': form,
                                                                'snippet': snippet})
    else:
        form = AddSnippetForm()
    return response(request, add_snippet_template, {'form': form})

@login_required
@is_snippetowner
def view_modify_snippet(request, snippet_id, snippet_slug, modify_snippet_template, snippet_profile_template):
    from quest.forms import AddSnippetForm
    if request.method == 'POST':
        form_data = {'title':'',
                     'explanation':'',
                     'code':'',
                     'snippet':'',
                     'lang':''}
        form = AddSnippetForm(form_data)
        if form.is_valid():
            existing_snippet = Snippet.objects.get(id=snippet_id)
            updated_snippet = _handle_snippet_updation(form, existing_snippet)
            return response(request, snippet_profile_template, {'form': form,
                                                                'snippet': updated_snippet})
    else:
        form = AddSnippetForm()
        snippet = Snippet.objects.get(id=snippet_id)
        return response(request, modify_snippet_template, {'form':form,
                                                           'snippet': snippet})

def _handle_snippet_creation(form):
    snippet_data = form.cleaned_data
    title = snippet_data.get('title')
    code = snippet_data.get('code')
    explanation = snippet_data.get('explanation')
    public = snippet_data.get('public')
    lang = snippet_data.get('lang')
    return Snippet.objects.create_snippet(title=title,
                                             explanation=explanation,
                                             code=code,
                                             lang=lang,
                                             public=public)

def _handle_snippet_updation(form, existing_snippet):
    snippet_data = form.cleaned_data
    return Snippet.objects.update_snippet(existing_snippet, snippet_data)