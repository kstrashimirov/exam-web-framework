from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from travel.accounts.models import Profile, ProjectUser
from travel.web.models import Country, Resort, Review

UserModel = get_user_model()


class ProfileDetailsView(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123QwertY',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'picture': 'http://pic.jpg',
    }
    INVALID_CREDENTIALS = {
        'username': 'Test2',
        'password': '123QwertY'
    }
    VALID_REVIEW_DATA = {
        'name': 'Review',
        'grade': 'Poor',
        'resort_id': 1,
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

    # def test_when_open_not_existing_profile_return_error_404(self):
    #     response = self.client.get(reverse('profile details', kwargs={'pk': 1, }))
    #     self.assertEqual(404, response.status_code)
    #     """ Broken by exception middleware"""
    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return user, profile

    def __create_valid_user_profile_country_resort_and_review(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        country = Country.objects.create(
            **self.VALID_COUNTRY_DATA,
        )
        resort = Resort.objects.create(
            **self.VALID_RESORT_DATA,
            country=country,
            user=user,
        )
        review = Review.objects.create(
            **self.VALID_REVIEW_DATA,
            user=user,
        )
        return user, profile, country, resort, review

    def test_return_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse('profile details', kwargs={'pk': profile.pk, }))

        self.assertTemplateUsed('user-details.html')

    def test_when_user_is_owner_expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk, }))

        self.assertTrue(response.context['is_owner'])

    def test_when_user_has_reviews__expect_to_return_reviews(self):
        user, profile, country, resort, review = self.__create_valid_user_profile_country_resort_and_review()
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEquals(
            review.id,
            response.context['reviews'],
        )

    def test_when_user_is_not_owner_expect_is_owner_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        user2 = UserModel.objects.create_user(**self.INVALID_CREDENTIALS)
        profile2 = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user2, )
        self.client.login(**self.INVALID_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk, }))

        self.assertFalse(response.context['is_owner'])

    def test_when_user_has_reviews_should_return_reviews(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(0, response.context['reviews'])


class UserRegisterView(TestCase):
    def test_return_correct_template(self):
        self.client.get(reverse('register'))

        self.assertTemplateUsed('user-add.html')


class EditLoginView(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123QwertY',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'picture': 'http://pic.jpg',
    }

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return user, profile

    def test_return_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertTemplateUsed('user-update.html')