import datetime
from django import forms

from models import MyBio

BOOTS_ATTRS = {'class': 'form-control'}


class DateSelectorWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        years = [(year, year)
                 for year in range(1900, datetime.date.today().year-15)]
        _widgets = (
            forms.widgets.Select(attrs=attrs,
                                 choices=[(day, day)
                                          for day in range(1, 32)]),
            forms.widgets.Select(attrs=attrs,
                                 choices=[(month, month)
                                          for month in range(1, 13)]),
            forms.widgets.Select(attrs=attrs,
                                 choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                value_date = datetime.datetime.strptime(value,
                                                        "%Y-%m-%d").date()
            else:
                value_date = value
            return [str(value_date.day),
                    str(value_date.month),
                    str(value_date.year)]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files,
                                       name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = datetime.date(
                day=int(datelist[0]),
                month=int(datelist[1]),
                year=int(datelist[2]),
            )
        except ValueError:
            return ''
        else:
            return str(D)


class BioForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    birth_date = forms.DateField(
        widget=DateSelectorWidget(attrs=BOOTS_ATTRS))
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
