from rest_framework import serializers
from slot_machine.models import Word, Poem

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'text', 'created_at', 'modified_at')

class PoemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('id', 'text', 'words', 'handwriting_id', 'created_at', 'modified_at')
        depth = 1

class PoemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('id', 'text', 'words', 'handwriting_id', 'created_at', 'modified_at')
