from django.http import HttpResponse
from rest_framework import generics, mixins, status, views
from rest_framework.response import Response
from slot_machine.models import Word, Poem
from slot_machine.serializers import (
    WordSerializer,
    PoemCreateSerializer,
    PoemRetrieveSerializer,
)
from slot_machine.handwriting import Handwriting
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

class PoemPreview(views.APIView):
    """
    Preview text in handwriting via Handwriting.io API.
    ---
    """
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        handwriting_id = request.query_params.get('handwriting_id')
        type = request.query_params.get('type') or 'png'
        response = Handwriting(text=text, handwriting_id=handwriting_id).render(type)
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type')
        )

class PoemRender(generics.GenericAPIView):
    """
    Get rendered poem image or pdf.
    ---
    """
    queryset = Poem.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        type = request.query_params.get('type') or 'png'
        renderedPoem = instance.renderedpoem_set.filter(type=type).first()
        return HttpResponse(
            content=renderedPoem.content,
            status=status.HTTP_200_OK,
            content_type=renderedPoem.content_type()
        )

class HandwritingList(views.APIView):
    """
    Get list of handwritings via Handwriting.io API.
    ---
    """
    def get(self, request, *args, **kwargs):
        response = Handwriting.list()
        data = json.loads(response.text)
        return Response(data, status=response.status_code)

