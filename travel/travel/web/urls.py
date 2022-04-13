from django.contrib.auth.decorators import login_required
from django.urls import path, include

from travel.web.views import HomeView, add_country, remove_country, view_countries, add_resort, \
    view_all_resorts, remove_resort, edit_resort, view_resort, view_country, add_review, view_all_reviews, view_reviews, \
    remove_review, dashboard, group_permission

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', dashboard, name='dashboard'),

    path('country/add/', add_country, name='add country'),
    path('country/remove/<int:pk>/', remove_country, name='remove country'),
    path('country/', view_countries, name='countries'),
    path('country/view/<int:pk>', view_country, name='view country'),

    path('resorts/add/', add_resort, name='add resort'),
    path('resorts/', view_all_resorts, name='resorts'),
    path('resorts/remove/<int:pk>/', remove_resort, name='remove resort'),
    path('resorts/edit/<int:pk>/', edit_resort, name='edit resort'),
    path('resorts/view/<int:pk>/', view_resort, name='view resort'),

    path('reviews/add/', add_review, name='add review'),
    path('reviews/all/<int:pk>/', view_all_reviews, name='reviews'),
    path('reviews/<int:pk>/', view_reviews, name='view review'),
    path('reviews/remove/<int:pk>/', remove_review, name='remove review'),

    path('permission', group_permission, name='group'),
)