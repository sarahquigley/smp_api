from django.http import HttpResponse
from rest_framework import generics, mixins, status, views
from rest_framework.response import Response
from slot_machine.models import Word, Poem
from slot_machine.serializers import (
    WordSerializer,
    PoemCreateSerializer,
    PoemRetrieveSerializer,
)
import json

class SlotMachineSubmitView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        results = self.get_serializer(self.get_queryset(), many=True)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'results': results.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class WordList(generics.ListAPIView):
    """
    List words.
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
            return self.model.objects.filter(
                pk__in=self.request.query_params.getlist('pk__in')
            )
        return self.model.objects.all()


class WordSubmit(SlotMachineSubmitView):
    """
    Create words, get 3 random words.
    ---
    """
    queryset = Word.objects.random(3)
    serializer_class = WordSerializer


class PoemSubmit(SlotMachineSubmitView):
    """
    Create poems, add relations to existing words, get a random poem.
    ---
    """
    queryset = Poem.objects.random(1)
    serializer_class = PoemCreateSerializer


class PoemRetrieve(generics.RetrieveAPIView):
    """
    Get poems by their primary key.
    """
    queryset = Poem.objects.all()
    serializer_class = PoemRetrieveSerializer
