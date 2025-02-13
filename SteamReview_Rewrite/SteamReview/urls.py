from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('GameSelection/', views.GameSelection, name='GameSelection'),
    path('NewReview/<int:app_id>/', views.NewReview, name='NewReview'),
    path('ReviewDetails/<int:pk>/', views.ReviewDetails, name='ReviewDetails'),
]
