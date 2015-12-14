from slot_machine.models import Word, Poem
from slot_machine.serializers import WordSerializer, PoemCreateSerializer, PoemRetrieveSerializer
from rest_framework import generics
import random

class RandomListAPIView(generics.ListAPIView):
    def get_queryset(self):
        limit = 1
        if 'limit' in self.request.query_params:
            limit = int(self.request.query_params['limit'])
        return self.model.objects.random(limit)

class WordList(generics.ListCreateAPIView):
    """
    List and create words.
    Specify primary keys of words to be listed with pk__in parameter.
    ---
    GET:
        parameters:
            - name: pk__in
              description: pks of words to be retrieved
              required: false
              type: integer
              allowMultiple: true
              paramType: query
    """
    serializer_class = WordSerializer
    model = Word

    def get_queryset(self):
        if 'pk__in' in self.request.query_params:
            return self.model.objects.filter(pk__in=self.request.query_params.getlist('pk__in'))
        return self.model.objects.all()

class WordRandom(RandomListAPIView):
    """
    List randomly selected words.
    Specify number of words to be randomly selected with limit parameter.
    ---
    GET:
        parameters:
            - name: limit
              description: number of random words to list
              required: false
              type: integer
              paramType: query
    """
    serializer_class = WordSerializer
    model = Word

class PoemCreate(generics.CreateAPIView):
    """
    Create poems and add relations to existing words.
    ---
    """
    queryset = Poem.objects.all()
    serializer_class = PoemCreateSerializer

class PoemRetrieve(generics.RetrieveAPIView):
    """
    Get poems by their primary key.
    """
    queryset = Poem.objects.all()
    serializer_class = PoemRetrieveSerializer

class PoemRandom(RandomListAPIView):
    """
    List randomly selected poems.
    Specify number of poems to be randomly selected with limit parameter.
    ---
    GET:
        parameters:
            - name: limit
              description: number of random poems to list
              required: false
              type: integer
              paramType: query
    """
    serializer_class = PoemRetrieveSerializer
    model = Poem
