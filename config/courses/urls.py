from django.urls import path

from .views import *

urlpatterns = [
    path('get-course-list/', CourseListView.as_view(), name='get-course-list'),
    path('get-course-detail/<int:pk>/', CourseDetailView.as_view(), name='get-course-detail'),
]