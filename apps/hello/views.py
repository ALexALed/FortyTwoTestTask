from django.shortcuts import Http404
from django.views.generic import TemplateView
from .models import MyBio


class MyBioView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(MyBioView, self).get_context_data(**kwargs)
        bio_data_count = MyBio.objects.count()
        if bio_data_count >= 1:
            context['object'] = MyBio.objects.all()[0]
        else:
            raise Http404

        return context
