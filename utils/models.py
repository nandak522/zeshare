from django.db import models
from django.db.models import Manager as BaseModelManager
from tagging.models import Tag as BaseTag
from tagging.models import TagManager as BaseTagManager

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_on']
        get_latest_by = 'created_on'