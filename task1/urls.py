from django.conf.urls import url, include
from .views import List
from . import views

urlpatterns = [
    url(r'^$', List.as_view(), name='list-view'),
    url(r'^filter', views.filter),
]
