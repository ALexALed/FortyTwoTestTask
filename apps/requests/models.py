from django.db import models
from django.utils import timezone


class RequestData(models.Model):
    http_request = models.CharField(max_length=200)
    remote_addr = models.GenericIPAddressField()
    date_time = models.DateTimeField()
    viewed = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return 'Request {0} from {1}'.format(self.http_request,
                                             self.remote_addr)

    def save(self, *args, **kwargs):
        if not self.id and not self.date_time:
            self.date_time = timezone.now()
        return super(RequestData, self).save(*args, **kwargs)
