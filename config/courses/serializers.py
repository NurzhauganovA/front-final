from rest_framework import serializers
from courses.models import Course


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