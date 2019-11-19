from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet, basename='movies')
router.register(r'comments', views.CommentViewSet, basename='comments')
urlpatterns = [
    url(r'^top/$', views.top_movies),
]
urlpatterns += router.urls