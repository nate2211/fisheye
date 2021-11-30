from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Image, Canvas, User
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = [ 'points', 't', 'outputImage', 'image_name', 'op']


class CanvasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['image_name', 'Cimage', 'canvasRectPoints']
