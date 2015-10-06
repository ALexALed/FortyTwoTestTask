from django.db import models


class MyBio(models.Model):
    first_name = models.CharField(u"Name", max_length=50)
    last_name = models.CharField(u"Last name", max_length=50)
    birth_date = models.DateField(u"Date of birth", blank=True, null=True)
    biography = models.TextField(u"Bio", blank=True, null=True)
    email = models.EmailField(u"email", blank=True, null=True)
    skype = models.CharField(u"Skype", max_length=200, blank=True, null=True)
    jabber = models.EmailField(u"Jabber", blank=True, null=True)
    other_contacts = models.TextField(u"Other contacts", blank=True, null=True)

    def __str__(self):
        return "Bio data for {0} {1}".format(self.first_name, self.last_name)
