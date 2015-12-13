from __future__ import unicode_literals

from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.word


class Poem(models.Model):
    text = models.TextField()
    words = models.ManyToManyField(Word)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
