from django.contrib.syndication.feeds import Feed
from quest.models import Snippet

class LatestSnippets(Feed):
    title = "Latest Snippets"
    link = "/feeds/snippets/"
    description = "Updates on latest snippets"
    description_template = 'snippets_description.html'
    
    def items(self):
        return Snippet.publicsnippets.all()