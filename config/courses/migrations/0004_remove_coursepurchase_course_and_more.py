# Generated by Django 5.1.4 on 2024-12-20 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_coursecart_user_alter_courselike_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursepurchase',
            name='course',
        ),
        migrations.RemoveField(
            model_name='shippingcertificate',
            name='certificate_image',
        ),
        migrations.RemoveField(
            model_name='shippingcertificate',
            name='certificate_number',
        ),
        migrations.RemoveField(
            model_name='shippingcertificate',
            name='course',
        ),
        migrations.RemoveField(
            model_name='shippingcertificate',
            name='user',
        ),
        migrations.AddField(
            model_name='coursepurchase',
            name='shipping_certificate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.shippingcertificate', verbose_name='Сертификат'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursepurchase',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Общая стоимость'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippingcertificate',
            name='delivery_time',
            field=models.PositiveIntegerField(default=1, verbose_name='Время доставки'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CourseCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_number', models.CharField(max_length=150, verbose_name='Номер сертификата')),
                ('certificate_image', models.FileField(upload_to='uploads/certificates/', verbose_name='Изображение сертификата')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('is_shipping', models.BooleanField(default=False, verbose_name='Доставлено')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='shippingcertificate',
            name='certificates',
            field=models.ManyToManyField(related_name='shipping_certificates', to='courses.coursecertificate', verbose_name='Сертификаты'),
        ),
    ]
