from django.conf.urls import url

from slot_machine.views import (
    WordList,
    WordSubmit,
    PoemSubmit,
    PoemPreview,
    PoemRetrieve,
    PoemRender,
    HandwritingList,
)

urlpatterns = [
    url(r'^word/$', WordList.as_view(), name='word-list'),
    url(r'^word/submit/$', WordSubmit.as_view(), name='word-submit'),
    url(r'^poem/submit/$', PoemSubmit.as_view(), name='poem-submit'),
    url(r'^poem/preview/$', PoemPreview.as_view(), name='poem-preview'),
    url(r'^poem/(?P<pk>[0-9]+)/$', PoemRetrieve.as_view(), name='poem-retrieve'),
    url(r'^poem/(?P<pk>[0-9]+)/render/$', PoemRender.as_view(), name='poem-render'),
    url(r'^handwriting/$', HandwritingList.as_view(), name='handwriting-list'),
]
