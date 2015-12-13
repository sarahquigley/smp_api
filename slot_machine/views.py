from slot_machine.models import Word, Poem
from slot_machine.serializers import WordSerializer, PoemCreateSerializer, PoemRetrieveSerializer
from rest_framework import generics
import random

class RandomListAPIView(generics.ListAPIView):
    def get_queryset(self):
        limit = 1
        if 'limit' in self.request.query_params:
            limit = int(self.request.query_params['limit'])
        if self.model.objects.count() < limit:
            limit = self.model.objects.count()
        return random.sample(self.model.objects.all(), limit)

class WordList(generics.ListCreateAPIView):
    serializer_class = WordSerializer
    model = Word

    def get_queryset(self):
        if 'pk__in' in self.request.query_params:
            return self.model.objects.filter(pk__in=self.request.query_params.getlist('pk__in'))
        return self.model.objects.all()

class WordRandom(RandomListAPIView):
    serializer_class = WordSerializer
    model = Word

class PoemCreate(generics.CreateAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemCreateSerializer

class PoemRetrieve(generics.RetrieveAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemRetrieveSerializer

class PoemRandom(RandomListAPIView):
    serializer_class = PoemRetrieveSerializer
    model = Poem
