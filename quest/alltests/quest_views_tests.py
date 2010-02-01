from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse, resolve as url_resolve
from quest.models import Snippet

class AllSnippetsPage_Tests(TestCase):
    fixtures = ['snippets.json']

    def test_all_snippets_url(self):
        response = self.client.get(url_reverse('quest.views.view_all_snippets'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        context = response.context[0]
        self.assertTrue(context.has_key('snippets'))
        snippets = context.get('snippets')
        self.assertTrue(hasattr(snippets, 'object_list'))
        self.assertTrue(snippets.object_list)
        self.assertTemplateUsed(response, 'all_snippets.html')

class SnippetProfilePage_Tests(TestCase):
    fixtures = ['snippets.json']

    def test_snippetprofile_url(self):
        snippet = Snippet.objects.all()[0]
        snippet_id = snippet.id
        snippet_slug = snippet.slug
        response = self.client.get(url_reverse('quest.views.view_snippet_profile',
                                               args=(snippet_id, snippet_slug)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        context = response.context[0]
        self.assertTrue(context.has_key('snippet'))
        snippet = context.get('snippet')
        self.assertEquals(snippet.id, snippet_id)
        self.assertEquals(snippet.slug, snippet_slug)

class AddSnippetPage_Tests(TestCase):
    fixtures = ['UserProfileTests.json']

    def test_addsnippet_url(self):
        response = self.client.get(url_reverse('quest.views.view_add_snippet'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_snippet.html')
        #TODO:Actually in Django 1.1, any context can be accessed in a generic way. 
        #context = response.context
        context = response.context[0]
        self.assertTrue(context.has_key('form'))
        form = context.get('form')
        self.assertFalse(form.errors)

    def test_addsnippet_anonymously(self):
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':True,
                     'lang':'py'}
        response = self.client.post(path=url_reverse('quest.views.view_add_snippet'), data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        context = response.context[0]
        snippet = context.get('snippet', None)
        self.assertTrue(snippet)
        self.assertEquals(snippet, Snippet.objects.latest())
        from quest.models import UserProfileSnippetMembership
        self.assertEquals(UserProfileSnippetMembership.objects.count(), 0)
        self.assertEquals(snippet.title, form_data.get('title'))
        self.assertEquals(snippet.explanation, form_data.get('explanation'))
        self.assertEquals(snippet.code, form_data.get('code'))
        self.assertTrue(snippet.public)
        self.assertEquals(snippet.lang, form_data.get('lang'))

    def test_addsnippet_after_logging_in(self):
        login_done = self.client.login(username='madhav.bnk@gmail.com', password='madhav')
        self.assertTrue(login_done)
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':True,
                     'lang':'py'}
        response = self.client.post(path=url_reverse('quest.views.view_add_snippet'), data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        context = response.context[0]
        snippet = context.get('snippet', None)
        self.assertTrue(snippet)
        from quest.models import UserProfileSnippetMembership
        self.assertEquals(UserProfileSnippetMembership.objects.count(), 1)
        membership = UserProfileSnippetMembership.objects.latest()
        self.assertEquals(membership.snippet, snippet)
        from users.models import UserProfile
        self.assertEquals(membership.userprofile, UserProfile.objects.get(email='madhav.bnk@gmail.com'))

    def test_create_snippet_with_invalid_data(self):
        form_data = {'title':'',
                    'explanation':'',
                    'code':'x=0',
                    'public':False,
                    'lang':'py'}
        response = self.client.post(url_reverse('quest.views.view_add_snippet'),
                                     form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_snippet.html')
        context = response.context[0]
        form = context.get('form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('title'))
        self.assertTrue(form.errors.get('explanation'))
        self.assertEquals(Snippet.objects.count(), 0)

class ModifySnippetPageTests(TestCase):
    fixtures = ['UserProfileTests.json']

    def test_modify_snippet_url(self):
        self.assertEquals(Snippet.objects.count(), 0)
        login_done = self.client.login(username='madhav.bnk@gmail.com', password='madhav')
        self.assertTrue(login_done)
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':False,
                     'lang':'py'}
        self.client.post(url_reverse('quest.views.view_add_snippet'),
                         form_data)
        snippet = Snippet.objects.latest()
        response = self.client.get(url_reverse('quest.views.view_modify_snippet',
                                               args=(snippet.id, snippet.slug)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_snippet.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.errors)
        self.assertEquals(form.cleaned_data.get('title'), form_data['title'])
        self.assertEquals(form.cleaned_data.get('explanation'), form_data['explanation'])
        self.assertEquals(form.cleaned_data.get('code'), form_data['code'])
        self.assertEquals(form.cleaned_data.get('lang'), form_data['lang'])
        self.assertFalse(form.cleaned_data.get('public'))

    def test_modify_snippet_successfully(self):
        login_done = self.client.login(username='madhav.bnk@gmail.com', password='madhav')
        self.assertTrue(login_done)
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':False,
                     'lang':'py'}
        self.client.post(url_reverse('quest.views.view_add_snippet'),
                         form_data)
        snippet = Snippet.objects.latest()
        self.assertEquals(snippet.title, form_data['title'])
        form_data['title'] = 'Updated:Some Snippet'
        response = self.client.post(url_reverse('quest.views.view_modify_snippet', args=(snippet.id, snippet.slug)), 
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        self.assertEquals(snippet, response.context[0].get('snippet'))
        snippet = Snippet.objects.latest()
        self.assertEquals(snippet.title, form_data['title'])

    def test_modify_snippet_with_invalid_data(self):
        login_done = self.client.login(username='madhav.bnk@gmail.com', password='madhav')
        self.assertTrue(login_done)
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':False,
                     'lang':'py'}
        self.client.post(url_reverse('quest.views.view_add_snippet'),
                         form_data)
        snippet = Snippet.objects.latest()
        form_data['title'] = ''
        response = self.client.post(url_reverse('quest.views.view_modify_snippet', args=(snippet.id, snippet.slug)), 
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_snippet.html')
        context = response.context[0]
        form = context.get('form')
        self.assertTrue(form.errors.get('title'))
        
class SnippetSearchPageTests(TestCase):
    fixtures = ['SnippetSearchPageTests.json']
    
    def test_search_snippetpage_url(self):
        response = self.client.get(path=url_reverse('quest.views.view_search_snippets'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_snippets.html')
        context = response.context[0]
        form = context.get('form', None)
        self.assertTrue(form)
        self.assertFalse(form.errors)
    
    def test_search_snippetpage_valid_submission(self):
        form_data = {'query': 'list'}
        response = self.client.post(path=url_reverse('quest.views.view_search_snippets'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_snippets.html')
        context = response.context[0]
        form = context.get('form', None)
        self.assertTrue(form)
        self.assertFalse(form.errors)
        search_results = context.get('snippets', [])
        self.assertTrue(search_results)
        snippets = search_results.object_list
        self.assertTrue(form_data['query'] in snippets[0]['slug'])
    
    def test_search_snippetpage_invalid_submission(self):
        response = self.client.post(path=url_reverse('quest.views.view_search_snippets'),
                                    data={'query': ''})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_snippets.html')
        context = response.context[0]
        form = context.get('form', None)
        self.assertTrue(form)
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('query'))