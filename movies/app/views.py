from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(username=email, email=email, password=password, full_name=full_name,
                                              phone_number=phone_number)
        login(request, user)
        return redirect('login')  # Redirect to the profile page after registration
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to profile page after login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def main(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(
            title__icontains=query) | Movie.objects.filter(
            genre__icontains=query) | Movie.objects.filter(
            actors__icontains=query) | Movie.objects.filter(
            summary__icontains=query)
    else:
        movies = Movie.objects.all()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(movies, 8)
    page_obj = paginator.get_page(page_number)

    return render(request, 'main.html', {
        'page_obj': page_obj,
        'query': query
    })

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'details.html', {'movie': movie})


@login_required
def add_to_watchlist(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    if movie not in user_watchlist.movies.all():
        user_watchlist.movies.add(movie)
        messages.success(request, f'"{movie.title}" has been added to your watchlist!')
    else:
        messages.info(request, f'"{movie.title}" is already in your watchlist.')
    return redirect('main')

@login_required
def watchlist_page(request):
    user = request.user
    watchlist = Movie.objects.filter(watchlist__user=user)
    return render(request, 'watchlist.html', {'watchlist': watchlist})


@login_required
def remove_from_watchlist(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    # Check if the movie is in the user's watchlist
    if movie in user_watchlist.movies.all():
        user_watchlist.movies.remove(movie)
        messages.success(request, f'"{movie.title}" has been removed from your watchlist.')
    else:
        messages.info(request, f'"{movie.title}" is not in your watchlist.')
    return redirect('main')

@login_required
def recommendation_page(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        language = request.POST.get('language')
        num_recommendations = int(request.POST.get('num_recommendations', 5))
        recommended_movies = Movie.objects.filter(
            genre__icontains=genre,
            languages__icontains=language
        ).order_by('-imdb_score')[:num_recommendations]

        return render(request, 'recommendations.html', {
            'recommended_movies': recommended_movies,
            'genre': genre,
            'language': language,
            'num_recommendations': num_recommendations
        })
    return render(request, 'recommendations_form.html')