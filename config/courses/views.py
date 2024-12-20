from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, CourseChapter, CourseReview, CourseRating, COURSE_CATEGORY, CourseCart, CourseLike
from courses.serializers import CourseSerializer, CourseDetailSerializer, CoureChapterSerializer, \
    CourseReviewSerializer, CourseAddReviewSerializer, CourseAddReviewAndRatingSerializer, CourseCreateSerializer, \
    CreateCourseChapterSerializer, CategorySerializer, AddToCartSerializer, RemoveFromCartSerializer, CartSerializer, \
    FavoriteSerializer, CourseCartSerializer


class CategoryListView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        return dict(COURSE_CATEGORY)

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        return Response(self.get_object())


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = None

    @swagger_auto_schema(
        tags=["courses"],
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.all()
        category = self.request.query_params.get('category')
        title = self.request.query_params.get('title')

        if category:
            queryset = queryset.filter(category=category)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({'message': 'Курс успешно создан'}, status=201)


class CourseChapterCreateView(generics.CreateAPIView):
    serializer_class = CreateCourseChapterSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Глава успешно создана'}, status=201)


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


class AddToCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not CourseCart.objects.filter(user=user).exists():
            CourseCart.objects.create(user=user)

        if course_id in user.cart.courses.values_list('id', flat=True):
            return Response({'message': 'Курс уже добавлен в корзину'}, status=400)

        course = get_object_or_404(Course, pk=course_id)
        user.cart.courses.add(course)

        return Response({'message': 'Курс успешно добавлен в корзину'})


class AddToFavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if course_id in user.likes.values_list('id', flat=True):
            return Response({'message': 'Курс уже добавлен в избранное'}, status=400)

        course = get_object_or_404(Course, pk=course_id)
        CourseLike.objects.create(user=user, course=course)

        return Response({'message': 'Курс успешно добавлен в избранное'})


class RemoveFromCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course = get_object_or_404(Course, pk=course_id)
        user.cart.courses.remove(course)

        return Response({'message': 'Курс успешно удален из корзины'})


class RemoveFromFavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course = get_object_or_404(Course, pk=course_id)
        CourseLike.objects.filter(user=user, course=course).delete()

        return Response({'message': 'Курс успешно удален из избранного'})


class CartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        cart = request.user.cart
        serializer = self.serializer_class(cart, context={'request': request})
        return Response(serializer.data)


class FavoriteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseCartSerializer

    @swagger_auto_schema(tags=["courses"])
    def get(self, request, *args, **kwargs):
        likes = request.user.likes.all()
        courses = [like.course for like in likes]
        serializer = self.serializer_class(courses, many=True, context={'request': request})
        return Response(serializer.data)
