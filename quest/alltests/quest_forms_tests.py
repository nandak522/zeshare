from utils import TestCase
from quest.forms import SearchSnippetForm
from quest.forms import AddSnippetForm

class AddSnippetFormTests(TestCase):
    def test_add_snippet_form_valid_submission(self):
        form_data = {'title':'Can anybody improve this Imports_Checker',
                     'explanation':'Something goes in here',
                     'code':'''Hey this is nothing''',
                     'public':True,
                     'lang':'py'}
        form = AddSnippetForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data)
        self.assertEquals(form.cleaned_data.get('title'), form_data['title'])
        self.assertEquals(form.cleaned_data.get('explanation'), form_data['explanation'])
        self.assertEquals(form.cleaned_data.get('code'), form_data['code'])
        self.assertTrue(form.cleaned_data.get('public'))
        self.assertEquals(form.cleaned_data.get('lang'), form_data['lang'])

    def test_add_snippet_form_invalid_submission(self):
        form_data = {'title':'',
                     'explanation':'',
                     'code':'''''',
                     'public':None,
                     'lang':'py'}
        form = AddSnippetForm(form_data)
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('title'))
        self.assertTrue(form.errors.get('explanation'))
        self.assertTrue(form.errors.get('code'))
        
class SearchSnippetFormTests(TestCase):
    def test_search_snippet_form_valid_submission(self):
        form_data = {'query': 'loop'}
        form = SearchSnippetForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data)
        cleaned_data = form.cleaned_data
        self.assertEquals(cleaned_data.get('query'), form_data['query'])
        
    def test_search_snippet_form_invalid_submission(self):
        form_data = {'query': ''}
        form = SearchSnippetForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('query'))