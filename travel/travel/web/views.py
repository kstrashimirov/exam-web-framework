from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import generic as views
from django.shortcuts import render, redirect

from travel.accounts.models import ProjectUser
from travel.common.decorators import allowed_groups
from travel.common.view_mixin import RedirectToDashboard
from travel.web.forms import CreateCountryForm, DeleteCountryForm, CreateResortForm, EditResortForm, DeleteResortForm, \
    CreateReviewForm
from travel.web.models import Country, Resort, Review


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


#
# class DashboardView(views.TemplateView):
#     reviews = Reviews.objects.all()
#     template_name = 'dashboard.html'


@login_required
def dashboard(request):
    country = len(Country.objects.all())
    reviews = len(Review.objects.all())
    resorts = len(Resort.objects.all())

    context = {
        'reviews': reviews,
        'resorts': resorts,
        'country': country,
    }
    return render(request, 'dashboard.html', context)


@allowed_groups(['admin', 'backoffice'])
def add_country(request):
    if request.method == "POST":
        form = CreateCountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CreateCountryForm()
    context = {
        'form': form,
    }
    return render(request, 'web/add_country.html', context)


@allowed_groups(['admin', 'backoffice'])
def remove_country(request, pk):
    country = Country.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteCountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = DeleteCountryForm(instance=country)
    context = {
        'form': form,
        'country': country,
    }
    return render(request, 'web/remove_country.html', context)


def view_countries(request):
    p = Paginator(Country.objects.all(), 2)
    page = request.GET.get('page')
    countries = p.get_page(page)

    context = {
        'countries': countries,
    }
    return render(request, 'web/countries.html', context)


def view_country(request, pk):
    country = Country.objects.get(pk=pk)
    resorts = Resort.objects.filter(country_id=pk)

    resorts_count = len(resorts)
    context = {
        'country': country,
        'resorts_count': resorts_count,
    }
    return render(request, 'web/view_country.html', context)


@allowed_groups(['admin', 'backoffice'])
def add_resort(request):
    if request.method == "POST":
        form = CreateResortForm(request.POST)
        if form.is_valid():
            resort = form.save(commit=False)
            resort.user = request.user
            resort.save()
            return redirect('countries')
    else:
        form = CreateResortForm()
    context = {
        'form': form,
    }
    return render(request, 'web/add_resort.html', context)


def view_all_resorts(request):
    countries = Country.objects.all()
    # resorts = Resort.objects.all()

    p = Paginator(Resort.objects.all(), 1)
    page = request.GET.get('page')
    resorts = p.get_page(page)

    context = {
        'countries': countries,
        'resorts': resorts,
    }
    return render(request, 'web/resorts.html', context)


def view_resort(request, pk):
    resort = Resort.objects.get(pk=pk)
    reviews = Review.objects.filter(resort_id=pk)
    total = 0
    for review in reviews:
        if review.grade == "Excellent":
            total += 6
        elif review.grade == "Good":
            total += 4
        elif review.grade == "Poor":
            total += 3
        elif review.grade == "Bad":
            total += 2

    reviews_count = len(reviews) if reviews else 0
    score = total / reviews_count if reviews else "-No Reviews Yet-"

    is_owner = request.user.id == resort.user_id

    context = {
        'resort': resort,
        'reviews_count': reviews_count,
        'score': score,
        'is_owner': is_owner,
    }
    return render(request, 'web/view_resort.html', context)


@allowed_groups(['admin', 'backoffice'])
def edit_resort(request, pk):
    resort = Resort.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditResortForm(request.POST, instance=resort)
        if form.is_valid():
            form.save()
            return redirect('resorts')
    else:
        form = EditResortForm(instance=resort)
    context = {
        'form': form,
        'resort': resort,
    }
    return render(request, 'web/edit_resort.html', context)


@allowed_groups(['admin', 'backoffice'])
def remove_resort(request, pk):
    resort = Resort.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteResortForm(request.POST, instance=resort)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = DeleteResortForm(instance=resort)
    context = {
        'form': form,
        'resort': resort,
    }
    return render(request, 'web/remove_resort.html', context)


@login_required
def add_review(request):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('resorts')
    else:
        form = CreateReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'web/add_review.html', context)


def view_all_reviews(request, pk):
    countries = Country.objects.get(pk=pk)
    resorts = Resort.objects.get(id=pk)
    reviews = Review.objects.filter(resort_id=pk)

    context = {
        'countries': countries,
        'resorts': resorts,
        'reviews': reviews,
    }
    return render(request, 'web/reviews.html', context)


@login_required
def view_reviews(request, pk):
    review = Review.objects.get(pk=pk)
    resort = Resort.objects.get(id=review.resort_id)

    context = {
        'review': review,
        'resort': resort,
    }
    return render(request, 'web/view_review.html', context)


def remove_review(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteResortForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = DeleteResortForm(instance=review)
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'web/remove_review.html', context)
