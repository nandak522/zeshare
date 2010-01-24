from django.test import TestCase

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