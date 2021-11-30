from django.urls import path, include
from rest_framework import routers
from backend import views

from rest_framework.urlpatterns import format_suffix_patterns



router = routers.DefaultRouter()
router.register(r'images', views.ImageView, 'image')
router.register(r'canvas', views.CanvasView, 'canvas')
router.register(r'search', views.CanvasSearchView, 'search')
router.register(r'users', views.UserViewSet, 'user')
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls'),)
]
