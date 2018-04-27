from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^keyword/$', KeyWordListView.as_view()),
    url(r'^keyword/create/$', KeyWordCreateView.as_view()),
    url(r'^search_task/$', SearchListView.as_view()),
    url(r'^search_task/create/$', SearchCreateView.as_view()),
    url(r'^search_task/(?P<pk>\d+)/$', SearchDetailView.as_view()),

]
