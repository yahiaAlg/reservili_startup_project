from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('booking/', views.booking_view, name='booking'),
    path('bookmark/', views.bookmark_view, name='bookmark'),
]