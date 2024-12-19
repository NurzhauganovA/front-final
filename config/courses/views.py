from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics

from courses.models import Course
from courses.serializers import CourseSerializer, CourseDetailSerializer


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
