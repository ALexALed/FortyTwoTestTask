from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django import template


register = template.Library()


@register.simple_tag(name='edit_link')
def edit_link(instance):
    content_type = ContentType.objects.get_for_model(instance.__class__)
    return urlresolvers.reverse("admin:%s_%s_change" %
                                (content_type.app_label, content_type.model),
                                args=(instance.id,))
