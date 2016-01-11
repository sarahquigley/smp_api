from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.db import transaction
from slot_machine.handwriting import Handwriting

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
    """
    text = models.TextField()
    words = models.ManyToManyField(Word)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    handwriting_id = models.CharField(max_length=50)
    objects = SlotMachineQuerySet.as_manager()

    def __unicode__(self):
        return self.text

    def render(self, type='png'):
        """
        Render poem via HandwritingIO API.
        """
        response = Handwriting(
            text=self.text,
            handwriting_id=self.handwriting_id
        ).render(type)
        # Should catch error responses here
        return RenderedPoem(poem=self, content=response.content, type=type)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Over-ride save method.
        Save two RenderedPoem records (png & pdf) on save of Poem.
        """
        super(Poem, self).save(*args, **kwargs)
        self.render('png').save()
        self.render('pdf').save()

class RenderedPoem(models.Model):
    """
    Poems rendered as PDFs or PNGs to the slot machine.
    """
    content = models.BinaryField()
    type = models.CharField(max_length=3)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def content_type(self):
        """
        Get correct content_type for HTTP responses returning RenderedPoems
        """
        if self.type == 'png':
            return 'image/png'
        else:
            return 'application/pdf'
