from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/<int:pk>', views.download_report, name='download_report'),
]