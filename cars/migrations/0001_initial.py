# Generated by Django 3.1 on 2021-05-16 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('title', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='cars_cover/')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='cars.brand')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Model_auth',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraTableForPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cars', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_price', to='cars.car')),
                ('model_auths', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_price', to='cars.model_auth')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='model_auth',
            field=models.ManyToManyField(related_name='model_auth', through='cars.ExtraTableForPrice', to='cars.Model_auth'),
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range'),
        ),
    ]