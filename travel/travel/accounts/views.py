from django.shortcuts import redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.urls import reverse_lazy

from travel.accounts.forms import CreateProfileForm
from travel.accounts.models import Profile
from travel.common.view_mixin import RedirectToDashboard
from travel.web.models import Country, Review


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'user-add.html'
    success_url = reverse_lazy('dashboard')


class UserLoginView(auth_views.LoginView):
    template_name = 'user-login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class EditProfileView(views.UpdateView):
    model = Profile
    template_name = 'user-update.html'
    success_url = reverse_lazy('dashboard')
    fields = [
        'email',
        'first_name',
        'last_name',
        'picture',
        'description',
    ]
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'change-password.html'


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'user-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object is a Profile instance
        reviews = len(Review.objects.filter(id=self.object.user_id))

        # pet_photos = PetPhoto.objects \
        #     .filter(tagged_pets__in=pets) \
        #     .distinct()
        #
        # total_likes_count = sum(pp.likes for pp in pet_photos)
        # total_pet_photos_count = len(pet_photos)

        context.update({
            # 'total_likes_count': total_likes_count,
            # 'total_pet_photos_count': total_pet_photos_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'reviews': reviews,
        })

        return context


class UserLogoutView(views.View):
    def get(self, request):
        logout(request)
        return redirect('index')
