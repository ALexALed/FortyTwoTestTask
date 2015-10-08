from django.conf.urls import url

from .views import RequestsView

urlpatterns = [
    url(r'^index/$', RequestsView.as_view(), name='requests'),
]

