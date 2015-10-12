from django.db import models, connection
from django.db.models.signals import post_init, post_save, post_delete


def signals_init(sender, **kwargs):
    save_signal(sender, 'init')


def signals_save(sender, **kwargs):
    save_signal(sender, 'save')


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


post_init.connect(signals_init, dispatch_uid='FortyTwoTestTask.logger')
post_save.connect(signals_save, dispatch_uid='FortyTwoTestTask.logger')
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
