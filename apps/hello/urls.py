from django.conf.urls import url

from .views import MyBioView, MyBioUpdate

urlpatterns = [
    url(r'^$', MyBioView.as_view(), name='home'),
    url(r'^update/(?P<pk>\d+)/$', MyBioUpdate.as_view(), name='update'),
]
