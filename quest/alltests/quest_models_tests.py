from django.test import TestCase

class SnippetTests(TestCase):
    fixtures = []

    def test_create_snippet(self):
        from quest.models import Snippet
        data = {'title': "Simple Script to remove duplicates from a list",
                'explanation': "Simple Script to remove duplicates from a list",
                'code':'filter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang':'py'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                    explanation=data['explanation'],
                                                    code=data['code'],
                                                    lang=data['lang'])
        self.assertTrue(snippet)
        snippet = Snippet.objects.get(id=snippet.id)#fresh fetch from db
        self.assertEquals(snippet.title, data['title'])
        self.assertEquals(snippet.explanation, data['explanation'])
        self.assertEquals(snippet.code, data['code'])
        self.assertEquals(snippet.lang, data['lang'])
        self.assertTrue(snippet.public)
        self.assertTrue(snippet.active)

    def test_create_snippet_with_html_attributes(self):
        from quest.models import Snippet
        data = {'title': "Simple <script>Script</script> to remove duplicates from a list",
                'explanation': "Simple <script>Script</script> to remove duplicates from a list",
                'code':'<script>alert("Go Boom!");</script>filter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang':'py'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                    explanation=data['explanation'],
                                                    code=data['code'],
                                                    lang=data['lang'])
        self.assertTrue(snippet)
        snippet = Snippet.objects.get(id=snippet.id)#fresh fetch from db
        self.assertEquals(snippet.title, "Simple Script to remove duplicates from a list")
        self.assertEquals(snippet.explanation, "Simple Script to remove duplicates from a list")
        self.assertEquals(snippet.code, 'alert("Go Boom!");filter(lambda obj: objects_list.count(obj) <= 1, objects_list)')
        self.assertEquals(snippet.lang, data['lang'])
        self.assertTrue(snippet.public)
        self.assertTrue(snippet.active)

    def test_update_snippet(self):
        from quest.models import Snippet
        data = {'title': "Simple Script to remove duplicates from a list",
                'explanation': "Simple Script to remove duplicates from a list",
                'code':'@updated\nfilter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang': 'py'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                    explanation=data['explanation'],
                                                    code=data['code'],
                                                    lang=data['lang'])
        data = {'title': "<h1>Updated</h1> Simple Script to remove duplicates from a list",
                'explanation': "Updated Simple Script to remove duplicates from a list",
                'code':'#updated\nfilter(lambda obj: objects_list.count(obj) <= 1, objects_list)'}
        updated_snippet = Snippet.objects.update_snippet(snippet=snippet,
                                                            title=data['title'],
                                                            explanation=data['explanation'],
                                                            code=data['code'],
                                                            public=False,
                                                            active=False)
        self.assertEquals(updated_snippet.title, "Updated Simple Script to remove duplicates from a list")
        self.assertEquals(updated_snippet.explanation, data['explanation'])
        self.assertEquals(updated_snippet.code, data['code'])
        self.assertFalse(updated_snippet.active)
        self.assertFalse(updated_snippet.public)