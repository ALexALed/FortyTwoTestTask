from django.db import models


class RequestData(models.Model):
    http_request = models.CharField(max_length=200)
    remote_addr = models.GenericIPAddressField()
    date_time = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return 'Request {0} from {1}'.format(self.http_request,
                                             self.remote_addr)
