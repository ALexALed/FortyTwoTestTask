from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import MyBio


class MyBioView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(MyBioView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(MyBio, pk=1)
        return context


