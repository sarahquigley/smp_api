from django.conf.urls import url

from slot_machine.views import WordList, WordRandom, PoemCreate, PoemRetrieve, PoemRandom

urlpatterns = [
    url(r'^word/$', WordList.as_view(), name='word-list'),
    url(r'^word/random/$', WordRandom.as_view(), name='word-random'),
    url(r'^poem/$', PoemCreate.as_view(), name='poem-create'),
    url(r'^poem/random/$', PoemRandom.as_view(), name='poem-random'),
    url(r'^poem/(?P<pk>[0-9]+)/$', PoemRetrieve.as_view(), name='poem-retrieve'),
]
