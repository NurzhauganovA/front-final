from django.db import models

from authenticate.models import User


COURSE_CATEGORY = (
    ('adobe photoshop', 'Adobe Photoshop'),
    ('adobe illustrator', 'Adobe Illustrator'),
    ('ui/ux design', 'UI/UX Design'),
    ('web development', 'Web Development'),
    ('mobile development', 'Mobile Development'),
    ('data science', 'Data Science'),
    ('Game development', 'Game Development')
)


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(max_length=150, verbose_name='Категория', choices=COURSE_CATEGORY)
    image = models.ImageField(upload_to='uploads/courses/', verbose_name='Изображение курса')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_category_display(self):
        return dict(COURSE_CATEGORY)[self.category]

    def get_average_rating(self):
        ratings = CourseRating.objects.filter(course=self)
        if ratings:
            return round(sum([rating.rating for rating in ratings]) / len(ratings), 1)
        return 0

    def get_count_ratings(self):
        return CourseRating.objects.filter(course=self).count()

    def get_first_price(self):
        first_price = 110 * self.price / 100
        return first_price


class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=150, verbose_name='Название главы')
    description = models.TextField(verbose_name='Описание главы')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Глава курса'
        verbose_name_plural = 'Главы курсов'

    def __str__(self):
        return self.title


class CourseLesson(models.Model):
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, verbose_name='Глава')
    title = models.CharField(max_length=150, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отзыв')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')

    class Meta:
        ordering = ['id']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f"{self.course.title} - {self.rating}"


class CoursePurchase(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        ordering = ['id']
        verbose_name = 'Покупка курса'
        verbose_name_plural = 'Покупки курсов'

    def __str__(self):
        return self.course.title


class CourseLike(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        ordering = ['id']
        verbose_name = 'Лайк курса'
        verbose_name_plural = 'Лайки курсов'

    def __str__(self):
        return self.course.title
