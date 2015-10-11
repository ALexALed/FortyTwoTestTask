from django.conf.urls import url

from .views import MyBioView, MyBioUpdate, create_superuser

urlpatterns = [
    url(r'^$', MyBioView.as_view(), name='home'),
    url(r'^update/(?P<pk>\d+)/$', MyBioUpdate.as_view(), name='update'),
    url(r'^create-superuser/$', create_superuser, name='create_superuser'),
]
