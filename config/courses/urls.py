from django.urls import path

from .views import *

urlpatterns = [
    path('get-course-list/', CourseListView.as_view(), name='get-course-list'),
    path('get-course-detail/<int:pk>/', CourseDetailView.as_view(), name='get-course-detail'),
    path('get-chapter-lessons/<int:pk>/', ChapterLessonsView.as_view(), name='get-chapter-lessons'),

    path('add-review-and-rating/', AddReviewAndRatingView.as_view(), name='add-review-and-rating'),
]