from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('GameSelection/', views.GameSelection, name='GameSelection'),
    path('NewReview/', views.NewReview, name='NewReview'),
]
