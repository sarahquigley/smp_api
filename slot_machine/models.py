from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.db import transaction

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
    """
    Words submitted to the slot machine.
    """
    text = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=ur'^[\-a-zA-Z\u00C0-\u017F]{1,255}$',
                message='Enter one word without spaces or punctuation.'
            ),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = SlotMachineQuerySet.as_manager()

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        """
        Over-ride save method.
        Ensure word text is lowercase before save.
        """
        self.text = self.text.lower()
        super(Word, self).save(*args, **kwargs)


class Poem(models.Model):
    """
    Poems submitted to the slot machine.
    Note: currently files are stored directly in the database in a BinaryField.
    This was a handy quick solution for the proof of concept app.
    It should not be the solution used in the final production ready app.
    """
    text = models.TextField()
    words = models.ManyToManyField(Word)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = SlotMachineQuerySet.as_manager()

    def __unicode__(self):
        return self.text
