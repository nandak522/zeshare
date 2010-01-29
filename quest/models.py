from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.template.defaultfilters import striptags
from pygments import formatters
from pygments import highlight as syntax_highlight
from pygments.lexers import get_lexer_by_name
from users.models import UserProfile
from utils import language_choices
from utils.models import BaseModel, BaseModelManager
from django.template.defaultfilters import slugify

class UserAlreadyCreatedSnippetException(Exception):
    pass

class ActiveSnippetManager(models.Manager):
    def get_query_set(self):
        return super(ActiveSnippetManager, self).get_query_set().filter(active=True)

class PublicSnippetManager(models.Manager):
    def get_query_set(self):
        return super(PublicSnippetManager, self).get_query_set().filter(public=True)

class SnippetManager(models.Manager):
    def create_snippet(self, title, explanation, code, lang, public=True, active=True):
        title = striptags(title)
        explanation = striptags(explanation)
        code = striptags(code)
        snippet = Snippet(title=title, slug=slugify(title), explanation=explanation, code=code, lang=lang, public=public, active=active)
        snippet.save()
        return snippet

    def update_snippet(self, existing_snippet, **params):
        for key,value in params.items():
            if isinstance(value, str) or isinstance(value, unicode):
                params[key] = striptags(value)
        for param in params:
            setattr(existing_snippet, param, params[param])
        existing_snippet.save()
        return Snippet.objects.get(id=existing_snippet.id)

class Snippet(BaseModel):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    explanation = models.TextField(max_length=200)
    code = models.TextField(max_length=1500)
    lang = models.CharField(max_length=10, choices=language_choices)
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    objects = SnippetManager()
    publicsnippets = PublicSnippetManager()
    activesnippets = ActiveSnippetManager()

    def __unicode__(self):
        return self.title
    
    def get_owner(self):
        try:
            return UserProfileSnippetMembership.objects.get(snippet=self).userprofile
        except UserProfileSnippetMembership.DoesNotExist:
            return AnonymousUser()
    
    owner = property(get_owner)
    
    def save(self, force_insert=False, force_update=False):
        self.title = striptags(self.title)
        self.explanation = striptags(self.explanation)
        self.code = striptags(self.code)
        super(Snippet, self).save(force_insert=force_insert, 
                                  force_update=force_update)
        
    def get_lexer(self):
        if self.lang == 'py':
            return get_lexer_by_name('python')
        elif self.lang == 'sql':
            return get_lexer_by_name('sql')
        elif self.lang == 'js':
            return get_lexer_by_name('js')
        elif self.lang == 'html':
            return get_lexer_by_name('html')
        else:
            raise NotImplementedError 
    
    def highlight(self):
        return syntax_highlight(self.code,
                                self.get_lexer(),
                                formatters.HtmlFormatter(linenos='table', 
                                                         lineanchors='line',
                                                         anchorlinenos=True))

    def activate(self):
        if not self.active:
            self.active = True
            self.save()
            return self
        return None

    def close(self):
        if self.active:
            self.active = False
            self.save()
            return self
        return None

    deactivate = close

    def hide(self):
        if self.public:
            self.public = False
            self.save()
            return self
        return None

    private = hide

    def make_public(self):
        if not self.public:
            self.public = True
            self.save()
            return self
        return None

    def toggle_visibility(self):
        self.public = not self.public
        self.save()
        return self
    
class UserProfileSnippetMembershipManager(BaseModelManager):
    def create_membership(self, userprofile, snippet):
        if self.exists(userprofile=userprofile, snippet=snippet):
            raise UserAlreadyCreatedSnippetException
        membership = UserProfileSnippetMembership(userprofile=userprofile,
                                                  snippet=snippet)
        membership.save()
        return membership
    
    def exists(self, userprofile, snippet):
        if self.filter(userprofile=userprofile, snippet=snippet).count():
            return True
        return False
    
class UserProfileSnippetMembership(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    snippet = models.ForeignKey(Snippet)
    objects = UserProfileSnippetMembershipManager()
    
    def __unicode__(self):
        return self.userprofile, self.snippet.slug