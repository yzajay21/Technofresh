
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit
# Create your models here.

def image_upload_to(instance, filename):
    title = instance.Photo.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "products/%s/%s" %(slug, new_filename)


class Photo(models.Model):
    title = models.CharField(max_length=100)
    width = models.IntegerField(default=1380)
    height = models.IntegerField(default=450)
    image = models.ImageField(null="False",blank="False",upload_to='mediafiles')
    image_banner    = ImageSpecField(source='image',processors=[ResizeToFill(1350, 450)],format='JPEG',options={'quality':80})
    def __str__(self):
        return self.title
class Meta :
    ordering = ["title"]

