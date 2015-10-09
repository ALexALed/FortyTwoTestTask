from django.conf.urls import url

from .views import RequestsView, RequestsData

urlpatterns = [
    url(r'^index/$', RequestsView.as_view(), name='requests'),
    url(r'^requestsData/$', RequestsData.as_view(), name='requests_data'),
]
