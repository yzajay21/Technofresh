from django.db import models

# Create your models here.
class Offer(models.Model):
    title = models.CharField(max_length=100)
    #width = models.IntegerField(default=1380)
    #height = models.IntegerField(default=450)
    image = models.ImageField(null="False",blank="False",upload_to='mediafiles')
    #image_banner    = ImageSpecField(source='image',processors=[ResizeToFill(1350, 450)],format='JPEG',options={'quality':80})
    def __str__(self):
        return self.title

class Meta:
	ordering = ["title"]

