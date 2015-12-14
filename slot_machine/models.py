from __future__ import unicode_literals
from django.db import models
import random

class SlotMachineQuerySet(models.QuerySet):

    def random(self, limit=1):
        """
        As stated in Django docs: https://docs.djangoproject.com/en/1.9/ref/models/querysets/#order-by
        Note: order_by('?') queries may be expensive and slow, depending on the database backend you're using.
        This method will be sufficient for our proof of concept app.
        Down the line, a better method will need to be sought, especially if performance becomes an issue.
        """
        return self.order_by('?')[:limit]

class Word(models.Model):
    word = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = SlotMachineQuerySet.as_manager()

    def __unicode__(self):
        return self.word


class Poem(models.Model):
    text = models.TextField()
    words = models.ManyToManyField(Word)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = SlotMachineQuerySet.as_manager()

    def __unicode__(self):
        return self.text
