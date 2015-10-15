from django import forms

from models import MyBio

BOOTS_ATTRS = {'class': 'form-control'}
DATE_FORMAT = "%m-%d-%y"


class CalendarWidget(forms.TextInput):
    class Media:
        js = ('js/jquery-ui.min.js',
              'js/datepicker.js')
        css = {'all': ('css/jquery-ui.min.css',
                       'css/theme.css')}


class BioForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    birth_date = forms.DateField(
        widget=CalendarWidget(attrs=BOOTS_ATTRS))
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
