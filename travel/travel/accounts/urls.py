from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from travel.accounts.views import UserLoginView, ProfileDetailsView, UserRegisterView, ChangeUserPasswordView, \
    EditProfileView, UserLogoutView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='profile update'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('index')), name='password_change_done'),
)