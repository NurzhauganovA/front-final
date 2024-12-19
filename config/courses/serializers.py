from rest_framework import serializers
from courses.models import *


class CourseReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = CourseReview
        fields = ('id', 'user', 'text', 'created_at')


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ('id', 'title', 'description')


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    category = serializers.CharField(source='get_category_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_ratings = serializers.IntegerField(source='get_count_ratings', read_only=True)
    first_price = serializers.DecimalField(source='get_first_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CourseDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    category = serializers.CharField(source='get_category_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_ratings = serializers.IntegerField(source='get_count_ratings', read_only=True)
    first_price = serializers.DecimalField(source='get_first_price', max_digits=10, decimal_places=2, read_only=True)
    reviews = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return CourseReviewSerializer(reviews, many=True).data

    def get_chapters(self, obj):
        chapters = obj.chapters.all()
        return CourseChapterSerializer(chapters, many=True).data
