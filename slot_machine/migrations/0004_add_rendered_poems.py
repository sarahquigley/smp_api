from django.db import migrations
from slot_machine.models import Poem

def add_rendered_poems(apps, schema_editor):
    for poem in Poem.objects.all():
        poem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('slot_machine', '0003_auto_20151216_2335'),
    ]

    operations = [
        migrations.RunPython(add_rendered_poems, reverse_code=migrations.RunPython.noop),
    ]
