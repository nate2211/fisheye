import json

from django.contrib.auth.models import User
from django.db import models
import os
from .scripts import RegionGrowing
from .scripts import boundingBox, canvasRectPoints
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


    def upload_to(instance, filename):
        return os.path.join(instance.canvas.image_name, filename)

    outputImage = models.ImageField(upload_to=upload_to)
    points = JSONField(null=True)
    t = models.IntegerField()

    def save(self, *args, **kwargs):
        points = json.loads(self.points)
        regions = []
        for x in range(len(points)):
            reg = RegionGrowing((points[x][0], points[x][1]), self.canvas.image, self.t)
            reg.regionGrow()
            regions.append(reg.region)
        region = []
        for r in regions:
            region = region + r
        region = list(dict.fromkeys(region))
        self.outputImage = boundingBox(region)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.canvas.image_name
