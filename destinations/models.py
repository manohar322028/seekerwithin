from django.db import models
import os

def destination_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/destinations/<destination_name>/images/<filename>
    return f'destinations/{instance.destination.name}/images/{filename}'

def thumbnail_image_path(instance, filename):
    # Save as MEDIA_ROOT/destinations/<destination_name>/thumbnail.<ext>
    extension = filename.split('.')[-1]
    return f'destinations/{instance.name}/thumbnail.{extension}'

class Destination(models.Model):
    # intro
    name = models.CharField(max_length=255)
    short_intro = models.TextField()
    detailed_info = models.TextField()

    # images
    thumbnail_image = models.ImageField(upload_to=thumbnail_image_path, null=True, blank=True)
    images = models.ManyToManyField('DestinationImage', related_name='destinations', blank=True)

    # location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # times 
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=destination_image_path)

    def __str__(self):
        return self.image.url
