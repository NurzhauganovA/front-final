from rest_framework import serializers
from courses.models import *


class CourseAddReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ('course', 'user', 'text')
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CourseReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = CourseReview
        fields = ('id', 'user', 'text', 'created_at')


class CourseChapterSerializer(serializers.ModelSerializer):
    count_lessons = serializers.IntegerField(source='get_count_lessons', read_only=True)

    class Meta:
        model = CourseChapter
        fields = ('id', 'title', 'description', 'count_lessons')


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


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ('id', 'title', 'description', 'video_url')


class CoureChapterSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = CourseChapter
        fields = ('id', 'lessons')

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return CourseLessonSerializer(lessons, many=True).data


class CourseAddReviewAndRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = CourseReview
        fields = ('course', 'user', 'text', 'rating')
        extra_kwargs = {
            'user': {'read_only': True}
        }
