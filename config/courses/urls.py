from django.urls import path

from .views import *

urlpatterns = [
    path('get-category-list/', CategoryListView.as_view(), name='get-category-list'),

    path('get-course-list/', CourseListView.as_view(), name='get-course-list'),
    path('get-course-detail/<int:pk>/', CourseDetailView.as_view(), name='get-course-detail'),
    path('get-chapter-lessons/<int:pk>/', ChapterLessonsView.as_view(), name='get-chapter-lessons'),

    path('add-course/', CourseCreateView.as_view(), name='add-course'),
    path('add-course-chapter/', CourseChapterCreateView.as_view(), name='add-course-chapter'),

    path('add-review-and-rating/', AddReviewAndRatingView.as_view(), name='add-review-and-rating'),

    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-favorite/', AddToFavoriteView.as_view(), name='add-to-favorite'),

    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('remove-from-favorite/', RemoveFromFavoriteView.as_view(), name='remove-from-favorite'),

    path('get-cart/', CartView.as_view(), name='get-cart'),
    path('get-favorite/', FavoriteView.as_view(), name='get-favorite'),
]