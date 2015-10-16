from django import forms

from .models import MyBio
from .widgets import CalendarWidget

BOOTS_ATTRS = {'class': 'form-control'}


class BioForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    birth_date = forms.DateField(
        widget=CalendarWidget(bootstrap=True))
    biography = forms.CharField(
        widget=forms.widgets.Textarea(attrs=BOOTS_ATTRS))
    skype = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    jabber = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    email = forms.EmailField(
        widget=forms.widgets.EmailInput(attrs=BOOTS_ATTRS))
    other_contacts = forms.CharField(
        widget=forms.widgets.Textarea(attrs=BOOTS_ATTRS))
    photo = forms.ImageField(required=False)

    class Meta:
        model = MyBio
