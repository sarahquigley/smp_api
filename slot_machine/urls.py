from django.conf.urls import url

from slot_machine.views import WordList, WordSubmit, PoemSubmit, PoemRetrieve

urlpatterns = [
    url(r'^word/$', WordList.as_view(), name='word-list'),
    url(r'^word/submit/$', WordSubmit.as_view(), name='word-submit'),
    url(r'^poem/submit/$', PoemSubmit.as_view(), name='poem-submit'),
    url(r'^poem/(?P<pk>[0-9]+)/$', PoemRetrieve.as_view(), name='poem-retrieve'),
]
