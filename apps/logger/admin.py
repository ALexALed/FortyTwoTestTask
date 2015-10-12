from django.contrib import admin

from .models import DbSignals


class DbSignalsModelForm(admin.ModelAdmin):
    fields = ('signal', 'model', 'date')
    list_display = ('signal', 'model', 'date')

admin.site.register(DbSignals, DbSignalsModelForm)
