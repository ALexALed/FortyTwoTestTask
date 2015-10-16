from django import forms


class CalendarWidget(forms.DateInput):

    def __init__(self, bootstrap=False, attrs=None):
        if bootstrap:
            final_attrs = {'class': 'calendar-widget form-control'}
        else:
            final_attrs = {'class': 'CalendarWidget'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(CalendarWidget, self).__init__(attrs=final_attrs, format='%m/%d/%Y')

    class Media:
        js = ('//code.jquery.com/jquery-1.11.3.min.js',
              'CalendarWidget/js/jquery-ui.min.js',
              'CalendarWidget/js/datepicker.js',)
        css = {'all': ('CalendarWidget/css/jquery-ui.min.css',
                       'CalendarWidget/css/theme.css')}
