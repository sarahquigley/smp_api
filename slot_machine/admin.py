from django.contrib import admin
from django import forms
from slot_machine.models import Word, Poem, RenderedPoem

class PoemForm(forms.ModelForm):
    words = forms.ModelMultipleChoiceField(queryset=Word.objects.all())

class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')

class PoemAdmin(admin.ModelAdmin):
    form = PoemForm
    list_display = ('text', 'created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')

class RenderedPoemAdmin(admin.ModelAdmin):
    list_display = ('poem', 'type', 'created_at', 'modified_at')
    readonly_fields = ('poem', 'type', 'created_at', 'modified_at')

admin.site.register(Word, WordAdmin)
admin.site.register(Poem, PoemAdmin)
admin.site.register(RenderedPoem, RenderedPoemAdmin)
