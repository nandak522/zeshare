from utils import TestCase
from quest.models import Snippet
from users.models import UserProfile

class SnippetCRUDTests(TestCase):
    fixtures = []

    def test_create_snippet(self):
        data = {'title': "Simple Script to remove duplicates from a list",
                'explanation': "Simple Script to remove duplicates from a list",
                'code':'filter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang':'py',
                'tags':'python list'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                 explanation=data['explanation'],
                                                 code=data['code'],
                                                 lang=data['lang'],
                                                 tags=data['tags'])
        self.assertTrue(snippet)
        snippet = Snippet.objects.get(id=snippet.id)#fresh fetch from db
        self.assertEquals(snippet.title, data['title'])
        self.assertEquals(snippet.explanation, data['explanation'])
        self.assertEquals(snippet.code, data['code'])
        self.assertEquals(snippet.lang, data['lang'])
        self.assertTrue(filter(lambda entered_tag:entered_tag in " ".join([tag.name for tag in snippet.tags()]) , data['tags'].split()))
        self.assertTrue(snippet.public)
        self.assertTrue(snippet.active)

    def test_create_snippet_with_html_attributes(self):
        data = {'title': "Simple <script>Script</script> to remove duplicates from a list",
                'explanation': "Simple <script>Script</script> to remove duplicates from a list",
                'code':'<script>alert("Go Boom!");</script>filter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang':'py',
                'tags':'python crazy'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                    explanation=data['explanation'],
                                                    code=data['code'],
                                                    lang=data['lang'],
                                                    tags=data['tags'])
        self.assertTrue(snippet)
        snippet = Snippet.objects.get(id=snippet.id)#fresh fetch from db
        self.assertEquals(snippet.title, "Simple Script to remove duplicates from a list")
        self.assertEquals(snippet.explanation, "Simple Script to remove duplicates from a list")
        self.assertEquals(snippet.code, 'alert("Go Boom!");filter(lambda obj: objects_list.count(obj) <= 1, objects_list)')
        self.assertEquals(snippet.lang, data['lang'])
        self.assertTrue(filter(lambda entered_tag:entered_tag in " ".join([tag.name for tag in snippet.tags()]) , data['tags'].split()))
        self.assertTrue(snippet.public)
        self.assertTrue(snippet.active)

    def test_update_snippet(self):
        data = {'title': "Simple Script to remove duplicates from a list",
                'explanation': "Simple Script to remove duplicates from a list",
                'code':'@updated\nfilter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'lang': 'py',
                'tags':'python imports'}
        snippet = Snippet.objects.create_snippet(title=data['title'],
                                                    explanation=data['explanation'],
                                                    code=data['code'],
                                                    lang=data['lang'],
                                                    tags=data['tags'])
        data = {'title': "<h1>Updated</h1> Simple Script to remove duplicates from a list",
                'explanation': "Updated Simple Script to remove duplicates from a list",
                'code':'#updated\nfilter(lambda obj: objects_list.count(obj) <= 1, objects_list)',
                'tags':'pythonista performance'}
        updated_snippet = Snippet.objects.update_snippet(existing_snippet=snippet,
                                                         title=data['title'],
                                                         explanation=data['explanation'],
                                                         code=data['code'],
                                                         public=False,
                                                         active=False,
                                                         tags=data['tags'])
        self.assertEquals(updated_snippet.title, "Updated Simple Script to remove duplicates from a list")
        self.assertEquals(updated_snippet.explanation, data['explanation'])
        self.assertEquals(updated_snippet.code, data['code'])
        self.assertFalse(updated_snippet.active)
        self.assertFalse(updated_snippet.public)
        self.assertTrue(filter(lambda entered_tag:entered_tag in " ".join([tag.name for tag in snippet.tags()]) , data['tags'].split()))

class SnippetUserProfileMembershipTests(TestCase):
    fixtures = ['UserProfileTests.json', 'snippets.json']

    def test_create_membership(self):
        snippet = Snippet.objects.get(id=1)
        userprofile = UserProfile.objects.get(email='madhav.bnk@gmail.com')
        from quest.models import UserProfileSnippetMembership
        membership = UserProfileSnippetMembership.objects.create_membership(userprofile=userprofile,
                                                                            snippet=snippet)
        self.assertTrue(membership)
        self.assertEquals(membership.userprofile, userprofile)
        self.assertEquals(membership.snippet, snippet)

    def test_create_duplicate_membership(self):
        snippet = Snippet.objects.get(id=1)
        userprofile = UserProfile.objects.get(email='madhav.bnk@gmail.com')
        from quest.models import UserProfileSnippetMembership
        UserProfileSnippetMembership.objects.create_membership(userprofile=userprofile,
                                                               snippet=snippet)
        #trying to create a duplicate membership
        from quest.models import UserAlreadyCreatedSnippetException
        self.assertRaises(UserAlreadyCreatedSnippetException,
                          UserProfileSnippetMembership.objects.create_membership,
                          userprofile=userprofile,
                          snippet=snippet)

    def test_snippet_owner(self):
        snippet = Snippet.objects.get(id=1)
        userprofile = UserProfile.objects.get(email='madhav.bnk@gmail.com')
        from quest.models import UserProfileSnippetMembership
        membership = UserProfileSnippetMembership.objects.create_membership(userprofile=userprofile,
                                                                            snippet=snippet)
        self.assertTrue(membership)
        owner = snippet.owner
        self.assertTrue(owner)
        self.assertEquals(owner.__class__, UserProfile)
        membership.delete()
        owner = snippet.owner
        self.assertTrue(owner)
        from quest.models import AnonymousUser
        self.assertEquals(owner.__class__, AnonymousUser)