from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse, resolve as url_resolve
from quest.models import Snippet

class SnippetsFeedsTests(TestCase):
    fixtures = ['snippets.json']
    
    def test_snippets_feeds_url(self):
        snippets_feed_response = self.client.get(url_reverse("django.contrib.syndication.views.feed",
                                    args=('snippets',)))
        self.assertTrue(snippets_feed_response)
        self.assertEquals(snippets_feed_response.status_code, 200)
        self.assertEquals(snippets_feed_response._headers.get('content-type')[1], "application/rss+xml")
        for snippet in Snippet.publicsnippets.all():
            self.assertTrue(snippet.title in snippets_feed_response.content)