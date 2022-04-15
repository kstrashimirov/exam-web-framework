from django.core.exceptions import ValidationError
from django.test import TestCase

from travel.accounts.models import ProjectUser
from travel.web.models import Country, Review, Resort


class CountryTests(TestCase):
    VALID_COUNTRY_DATA = {
        'name': 'Bulgaria',
        'banner': 'http://flag.jpg',
    }

    def test_country_create__when_name_is_not_unique__expect_success(self):
        country = Country(**self.VALID_COUNTRY_DATA)
        country.save()
        self.assertIsNotNone(country.pk)

    def test_country_create__when_name_is_not_unique__expect_fail(self):
        country = Country(**self.VALID_COUNTRY_DATA)
        country.save()
        country2 = Country(
            name='Bulgaria',
            banner=self.VALID_COUNTRY_DATA['banner'],
        )

        with self.assertRaises(ValidationError) as context:
            country2.full_clean()
            country2.save()

        self.assertIsNotNone(context.exception)

    def test_country__delete__expect_no_country(self):
        country = Country(**self.VALID_COUNTRY_DATA)
        country.save()
        country.delete()
        self.assertIsNone(country.pk)


class ReviewTests(TestCase):
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

    def test_review_create__when_name_contains_allowed_chars__expect_success(self):
        user, country, resort, review = self.__create_valid_user_country_resort_and_review()

        self.assertIsNotNone(review.pk)

    def test_review_create__when_name_contains_not_allowed_chars__expect_fail(self):
        user, country, resort = self.__create_valid_user_country_resort()
        name = 'B@nsko'
        review = Review(
            name=name,
            grade=self.VALID_REVIEW_DATA['grade'],
        )

        with self.assertRaises(ValidationError) as context:
            review.full_clean()
            review.save()

        self.assertIsNotNone(context.exception)

    def test_review__delete__expect_no_country(self):
        user, country, resort, review = self.__create_valid_user_country_resort_and_review()
        review.delete()

        self.assertIsNone(review.pk)


class ResortTests(TestCase):
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

    def test_resort_create__when_name_unique__expect_success(self):
        user, country, resort = self.__create_valid_user_country_resort()

        self.assertIsNotNone(resort.pk)

    def test_resort_create__when_name_not_unique__expect_fail(self):
        user, country, resort = self.__create_valid_user_country_resort()
        name = 'Bansko'
        resort2 = Resort(
            name=name,
            type=self.VALID_RESORT_DATA['type'],
            country=country,
            user=user
        )

        with self.assertRaises(ValidationError) as context:
            resort2.full_clean()
            resort2.save()

        self.assertIsNotNone(context.exception)

    def test_resort__delete__expect_no_country(self):
        user, country, resort = self.__create_valid_user_country_resort()
        resort.delete()

        self.assertIsNone(resort.pk)