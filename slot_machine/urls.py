from django.conf.urls import url

from slot_machine.views import WordList, WordRandom, PoemCreate, PoemRetrieve, PoemRandom

urlpatterns = [
    url(r'^word/$', WordList.as_view()),
    url(r'^word/random/$', WordRandom.as_view()),
    url(r'^poem/$', PoemCreate.as_view()),
    url(r'^poem/random/$', PoemRandom.as_view()),
    url(r'^poem/(?P<pk>[0-9]+)/$', PoemRetrieve.as_view()),
]
