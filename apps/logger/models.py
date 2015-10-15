from django.db import models, connection
from django.db.models.signals import pre_save, post_delete


def signals_save_create(sender, **kwargs):
    if not hasattr(kwargs['instance'], 'id'):
        return
    if kwargs['instance'].id:
        save_signal(sender, 'save')
    else:
        save_signal(sender, 'create')


def signals_delete(sender, **kwargs):
    save_signal(sender, 'delete')


def save_signal(sender, signal):
    table_exist = db_table_exists('logger_dbsignals')
    if sender.__name__ != 'DbSignals' and table_exist:
        obj = DbSignals()
        obj.model = sender.__name__
        obj.signal = signal
        obj.save()


def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()

pre_save.connect(signals_save_create, dispatch_uid='FortyTwoTestTask.logger')
post_delete.connect(signals_delete, dispatch_uid='FortyTwoTestTask.logger')


class DbSignals(models.Model):
    """
    table for signals saver
    """
    signal = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(blank=True, auto_now_add=True)

    def __unicode__(self):
        return '{0}-{1}-{2}'.format(self.signal, self.model, self.date)
