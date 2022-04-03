from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from travel.common.validators import validate_name_chars

UserModel = get_user_model()


class Country(models.Model):
    MAX_NAME_LENGTH = 15

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            validate_name_chars,
        ),
        unique=True,
    )

    banner = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Resort(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_TYPES_LENGTH = 30

    SKI = 'Ski Resort'
    BEACH = "Beach Resort"
    SPA = 'SPA Resort'
    WELLNESS = 'Wellness Resort'
    TREKING = 'Treking Resort'

    TYPES = [(x, x) for x in (SKI, BEACH, SPA, WELLNESS, TREKING)]

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Resort Name',
        unique=True,
    )

    type = models.CharField(
        max_length=MAX_TYPES_LENGTH,
        choices=TYPES,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    image = models.URLField(
        null=True,
        blank=True,
        verbose_name='Image URL',
    )
    price = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    MAX_NAME_LENGTH = 35
    MAX_GRADE_LENGTH = 15

    EXCELLENT = 'Excellent'
    GOOD = 'Good'
    POOR = 'Poor'
    BAD = 'Bad'

    GRADES = [(x, x) for x in (EXCELLENT, GOOD, POOR, BAD)]

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            validate_name_chars,
        ),
    )

    grade = models.CharField(
        max_length=MAX_GRADE_LENGTH,
        choices=GRADES,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    resort = models.ForeignKey(
        Resort,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
