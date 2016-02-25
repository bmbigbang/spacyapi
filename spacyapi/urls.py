from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'spacyapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/',include('home.urls')),
]
