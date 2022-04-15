from django.contrib import admin

from travel.web.models import Country, Resort, Review


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Resort)
class ResortPhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')


@admin.register(Review)
class ReviewsPhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'resort', 'user')