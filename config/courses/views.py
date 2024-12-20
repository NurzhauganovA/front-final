from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, CourseChapter, CourseReview, CourseRating
from courses.serializers import CourseSerializer, CourseDetailSerializer, CoureChapterSerializer, \
    CourseReviewSerializer, CourseAddReviewSerializer, CourseAddReviewAndRatingSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = None

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer

    def get_object(self):
        return get_object_or_404(Course, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChapterLessonsView(generics.RetrieveAPIView):
    serializer_class = CoureChapterSerializer

    def get_object(self):
        return get_object_or_404(CourseChapter, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AddReviewAndRatingView(generics.CreateAPIView):
    serializer_class = CourseAddReviewAndRatingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        course = get_object_or_404(Course, pk=data.get('course'))
        user = request.user
        text = data.get('text')
        rating = data.get('rating')

        review = CourseReview.objects.create(course=course, user=user, text=text)
        CourseRating.objects.create(course=course, user=user, rating=rating)

        return Response({'message': 'Отзыв успешно добавлен'})
