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
                                               args = [snippet_id, snippet_slug]))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        context = response.context[0]
        self.assertTrue(context.has_key('snippet'))
        snippet = context.get('snippet')
        self.assertEquals(snippet.id, snippet_id)
        self.assertEquals(snippet.slug, snippet_slug)
        
class AddSnippetPage_Tests(TestCase):
    fixtures = []
    
    def test_addsnippet_url(self):
        response = self.client.get(url_reverse('quest.views.view_add_snippet'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_snippet.html')
        context = response.context[0] # Actually in Django 1.1, any context can be accessed in a generic way
        self.assertTrue(context.has_key('form'))
        form = context.get('form')
        self.assertFalse(form.errors)
        
    def test_create_snippet(self):
        self.assertEquals(Snippet.objects.count(), 0)
        form_data = {'title':'Some Snippet',
                     'explanation':'Some Snippet',
                     'code':'x=0',
                     'public':False,
                     'lang':'py'}
        response = self.client.post(url_reverse('quest.views.view_add_snippet'),
                                    form_data)
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.errors)
        self.assertTemplateUsed(response, 'snippet_profile.html')
        self.assertEquals(Snippet.objects.count(), 1)
        snippet = Snippet.objects.latest('created_on')
        self.assertEquals(snippet.title, form_data.get('title'))
        self.assertEquals(snippet.explanation, form_data.get('explanation'))
        self.assertEquals(snippet.code, form_data.get('code'))
        self.assertFalse(snippet.public)