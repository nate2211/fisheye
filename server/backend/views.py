from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .models import Image, Canvas
from rest_framework import viewsets, generics
from .scripts import canvasRectPoints
from .serializers import ImageSerializer, CanvasSerializer, UserSerializer
from django.core.files.base import ContentFile
from rest_framework.response import Response
from django.views import generic
from django_filters import rest_framework as filters

class UserViewSet(viewsets.ModelViewSet): # new
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class CanvasSearchView(viewsets.ModelViewSet):
    queryset = Canvas.objects.all()
    serializer_class = CanvasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'image_name']


@method_decorator(csrf_exempt, name='dispatch')
class CanvasView(viewsets.ModelViewSet):
    queryset = Canvas.objects.all()
    serializer_class = CanvasSerializer


    def post(self, request):
        file = request.data['image']
        image_name = request.data['image_name']
        image_name = os.path.splitext(image_name)[0]
        canvas = Canvas.objects.create(image_name=image_name, Cimage=file, canvasRectPoints=None)


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request):
        output = request.data['file']
        points = request.data['points']
        name = request.data['name']
        t = request.data['t']
        op = request.data['op']
        image = Image.objects.create( points=points, t=t, outputImage=output, image_name=name, op=op)
