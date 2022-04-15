from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from travel.accounts.models import Profile, ProjectUser

UserModel = get_user_model()


class ProjectUserTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123Parola',
    }

    def test_profile_create__with_username__expect_success(self):
        user = ProjectUser(**self.VALID_USER_CREDENTIALS,)
        user.save()
        self.assertIsNotNone(user.pk)


class ProfileTests(TestCase):
    VALID_PROFILE_DATA = {
        'first_name': 'Me',
        'last_name': 'You',
        'picture':'http://pic.jpg',
    }
    VALID_USER_CREDENTIALS = {
        'username': 'Test',
        'password': '123Parola',
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

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = 'Name2'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        first_name = 'me$name'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'me name'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        user, profile = self.__create_valid_user_and_profile()
        profile.save()

        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, str(profile))