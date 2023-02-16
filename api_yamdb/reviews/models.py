from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class CategoryGenres(models.Model):
    """Abstract model for genres and categories."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(CategoryGenres):
    """ORM model for categories."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(CategoryGenres):
    """ORM model for genres."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """ORM model for titles"""

    name = models.TextField(max_length=256)
    #  Prevents creating titles with year in the future.
    year = models.IntegerField(
        validators=[MaxValueValidator(datetime.now().year)]
    )
    score = models.FloatField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        default=1.0
    )
    description = models.TextField(max_length=256, null=True, blank=True)
    genre = models.ManyToManyField(
        Genres,
        related_name='genre',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    @property
    def title_rating(self):
        return None   # Доделать


class Review(models.Model):
    """ORM model for review."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField(max_length=256)
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
