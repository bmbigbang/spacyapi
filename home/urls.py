from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tokenizer/.*$', views.tokenizer),
    url(r'^similarity/.*$', views.similarity),
    url(r'^lemma/.*$', views.lemma),
    url(r'^vector/.*$', views.vector),
    url(r'^filter/.*$', views.filter),

]
