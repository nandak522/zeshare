from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from utils.models import BaseModel, BaseModelManager
import hashlib

class UserProfileAlreadyExistsException(Exception):
    pass

class UserProfileManager(BaseModelManager):
    def create_userprofile(self, email, password, name=''):
        if self.exists(email=email):
            raise UserProfileAlreadyExistsException
        user = User.objects.create_user(username=self._compute_username(email),
                                        email=email,
                                        password=password)
        userprofile = UserProfile(user=user, email=email, name=name, slug=slugify(name))
        userprofile.save()
        return userprofile

    def _compute_username(self, email):
        return hashlib.sha1(email).hexdigest()[:30]

    def exists(self, **params):
        return self.filter(**params).count()
    
    def update_userprofile(self, existing_userprofile, **params):
        password = params.pop('password', '')
        if password:
            user = existing_userprofile.user 
            user.set_password(password)
            user.save()
        if params.has_key('name') and not params.pop('slug', ''):
            params['slug'] = slugify(params.get('name')) 
        for parameter in params:
            setattr(existing_userprofile, parameter, params.get(parameter))
        existing_userprofile.save()
        return existing_userprofile

class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True) 
    objects = UserProfileManager()
    
    def __unicode__(self):
        return self.email