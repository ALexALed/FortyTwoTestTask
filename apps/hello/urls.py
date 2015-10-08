from django.conf.urls import url

from .views import MyBioView

urlpatterns = [
    url(r'^$', MyBioView.as_view(), name='home'),
]
