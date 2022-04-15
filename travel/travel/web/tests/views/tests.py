from django.test import TestCase
from django.urls import reverse

from travel.accounts.models import ProjectUser
from travel.web.models import Country, Review, Resort


class CountryViewTests(TestCase):
    VALID_COUNTRY_DATA = {
        'name': 'Bulgaria',
        'banner': 'http://flag.jpg',
    }

    def test_view_country(self):
        country = Country.objects.create(**self.VALID_COUNTRY_DATA, )
        self.client.get(reverse('view country', kwargs={'pk': country.pk, }))

        self.assertTemplateUsed('web/view_country.html')


class ResortViewTests(TestCase):
    VALID_RESORT_DATA = {
        'name': 'Bansko',
        'type': 'Ski',
        'price': 12,
    }
    VALID_COUNTRY_DATA = {
        'name': 'Bulgaria',
        'banner': 'http://flag.jpg',
    }
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123QwertY',
    }

    def __create_user(self, **credentials):
        return ProjectUser(**self.VALID_USER_CREDENTIALS)

    def __create_valid_user_country_resort(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        country = Country.objects.create(
            **self.VALID_COUNTRY_DATA,
        )
        country.save()
        resort = Resort.objects.create(
            **self.VALID_RESORT_DATA,
            country=country,
            user=user,
        )
        resort.save()

        return user, country, resort

    def test_view_resort(self):
        user, country, resort = self.__create_valid_user_country_resort()
        self.client.get(reverse('view resort', kwargs={'pk': resort.pk, }))

        self.assertTemplateUsed('web/view_resort.html')

    def test_delete_resort(self):
        user, country, resort = self.__create_valid_user_country_resort()
        self.client.get(reverse('remove resort', kwargs={'pk':resort.pk, }))

        self.assertTemplateUsed('web/remove_resort.html')


class ReviewViewTests(TestCase):
    VALID_REVIEW_DATA = {
        'name': 'Bansko',
        'grade': 'Good',
    }
    VALID_RESORT_DATA = {
        'name': 'Bansko',
        'type': 'Ski',
        'price': 12,
    }
    VALID_COUNTRY_DATA = {
        'name': 'Bulgaria',
        'banner': 'http://flag.jpg',
    }
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123QwertY',
    }

    def __create_user(self, **credentials):
        return ProjectUser(**self.VALID_USER_CREDENTIALS)

    def __create_valid_user_country_resort_and_review(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        country = Country.objects.create(
            **self.VALID_COUNTRY_DATA,
        )
        country.save()
        resort = Resort.objects.create(
            **self.VALID_RESORT_DATA,
            country=country,
            user=user,
        )
        resort.save()
        review = Review.objects.create(
            **self.VALID_REVIEW_DATA,
            resort=resort,
            user=user,
        )
        review.save()
        return user, country, resort, review

    def test_view_review(self):
        user, country, resort, review = self.__create_valid_user_country_resort_and_review()
        self.client.get(reverse('view review', kwargs={'pk': review.pk, }))

        self.assertTemplateUsed('web/view_review.html')

    def test_delete_review(self):
        user, country, resort, review = self.__create_valid_user_country_resort_and_review()
        self.client.get(reverse('remove review', kwargs={'pk': review.pk, }))

        self.assertTemplateUsed('web/remove_review.html')