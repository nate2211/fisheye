import json

from django.contrib.auth.models import User
from django.db import models
import os
from .scripts import RegionGrowing, BoundingBox
from .scripts import canvasRectPoints
from .scripts import ImagetoUint8
from jsonfield import JSONField


# Create your models here.


class Canvas(models.Model):

    image_name = models.CharField(max_length=200)

    def upload_to(instance, filename):
        return os.path.join(instance.image_name, filename)

    Cimage = models.ImageField(upload_to=upload_to)
    canvasRectPoints = JSONField(null=True)

    def save(self, *args, **kwargs):
        points = canvasRectPoints(self.Cimage)
        self.canvasRectPoints = points
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image_name


class Image(models.Model):

    image_name = models.CharField(max_length=200)
    def upload_to(instance, filename):
        return os.path.join(instance.image_name, filename)

    outputImage = models.ImageField(upload_to=upload_to)
    points = JSONField(null=True)
    t = models.IntegerField()
    op = models.BooleanField()
    def save(self, *args, **kwargs):
        regions = []
        reg = RegionGrowing(self.points, self.outputImage, self.t)
        reg.regionGrow()
        image = reg.outPut()
        box = BoundingBox(image, reg.aRegion)
        self.outputImage = box.boundingBox(self.op)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image_name
