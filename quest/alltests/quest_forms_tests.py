from utils import TestCase

class AddSnippetFormTests(TestCase):
    def test_add_snippet_form_valid_submission(self):
        form_data = {'title':'Can anybody improve this Imports_Checker',
                     'explanation':'Something goes in here',
                     'code':'''Hey this is nothing''',
                     'public':True,
                     'lang':'py'}
        from quest.forms import AddSnippetForm
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
        from quest.forms import AddSnippetForm
        form = AddSnippetForm(form_data)
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('title'))
        self.assertTrue(form.errors.get('explanation'))
        self.assertTrue(form.errors.get('code'))