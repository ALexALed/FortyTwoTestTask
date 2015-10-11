import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import Http404, HttpResponse
from django.views.generic import TemplateView, UpdateView
from .models import MyBio
from .forms import BioForm


class AjaxableResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


class MyBioView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(MyBioView, self).get_context_data(**kwargs)
        bio_data_count = MyBio.objects.count()
        if bio_data_count >= 1:
            context['object'] = MyBio.objects.first()
        else:
            raise Http404

        return context


class MyBioUpdate(AjaxableResponseMixin, UpdateView):
    model = MyBio
    template_name = 'hello/update.html'
    form_class = BioForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyBioUpdate, self).dispatch(*args, **kwargs)
