from datetime import timezone

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint
from pytils.translit import slugify

User = get_user_model()


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from pytils.translit import slugify
            self.slug = slugify(self.title)
        super().save()


class Model_auth(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Car(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model_auth = models.ManyToManyField(Model_auth, through='ExtraTableForPrice', related_name='model_auth')
    image = models.ImageField(upload_to='cars_cover/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            current = timezone.now().strftime('%s')
            self.slug = slugify(self.title) + current
        super().save()


class ExtraTableForPrice(models.Model):
    cars = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars_price')
    model_auths = models.ForeignKey(Model_auth, on_delete=models.CASCADE, related_name='books_price')
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    text = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range'
            )
        ]


class Like(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)


