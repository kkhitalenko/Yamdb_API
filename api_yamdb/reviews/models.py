from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class CategoryGenres(models.Model):
    """Abstract model for genres and categories."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
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
    rating = models.FloatField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        null=True,
        blank=True
    )
    description = models.TextField(max_length=256, null=True, blank=True)
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """ORM model for review."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """ORM model for comment."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']


class GenreTitle(models.Model):
    """ORM model for genre-title relaton."""

    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre_id} {self.title_id}'
