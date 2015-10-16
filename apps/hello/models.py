from PIL import Image
from django.db import models


class MyBio(models.Model):
    first_name = models.CharField("Name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    birth_date = models.DateField("Date of birth", blank=True, null=True)
    biography = models.TextField("Bio", blank=True, null=True)
    email = models.EmailField("email", blank=True, null=True)
    skype = models.CharField("Skype", max_length=200, blank=True, null=True)
    jabber = models.EmailField("Jabber", blank=True, null=True)
    other_contacts = models.TextField("Other contacts", blank=True, null=True)
    photo = models.ImageField("Photo", upload_to='hello/photos/',
                              blank=True, null=True)

    def get_update_url(self):
        from django.core.urlresolvers import reverse
        return reverse('update', args=[str(self.id)])

    def __str__(self):
        return "Bio data for {0} {1}".format(self.first_name, self.last_name)

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        super(MyBio, self).save(force_insert, force_update,
                                using, update_fields)
        if self.photo:
            self.resize_photo((200, 200))

    def resize_photo(self, size):
        image = Image.open(self.photo.path)
        image.thumbnail(size, Image.ANTIALIAS)
        #offset_x = max((size[0] - image.size[0]) / 2, 0)
        #offset_y = max((size[1] - image.size[1]) / 2, 0)
        #final_thumb = Image.new(mode='RGBA',
        #                        size=size,
        #                        color=(255, 255, 255, 0))

        #final_thumb.paste(image, (offset_x, offset_y))
        #image.widh
        image.save(self.photo.path, 'PNG')
