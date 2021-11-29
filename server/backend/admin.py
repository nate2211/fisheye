from django.contrib import admin

from .models import Image
from .models import Canvas


class CanvasAdmin(admin.ModelAdmin):
    list_display = ( 'image_name', 'Cimage', 'id', 'canvasRectPoints')


admin.site.register(Image)
admin.site.register(Canvas, CanvasAdmin)
# Register your models here.
