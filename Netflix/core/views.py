from multiprocessing import context
from sys import exec_prefix
from django.shortcuts import redirect, render
from django.views import View
from .models import Movie, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import JsonResponse
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('listProfile')
    return render(request, 'core/index.html')

@login_required(login_url='account_login')
def profile_list(request):
    profiles = request.user.profiles.all()
    context = {'profiles': profiles}
    return render(request, 'core/profile_list.html', context)


@login_required(login_url='account_login')
def profile_create(request):
    form = ProfileForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        age_limit = form.cleaned_data['age_limit']
        profile = Profile.objects.create(name=name, age_limit=age_limit)
        if profile:
            request.user.profiles.add(profile)
      
    context = {'form': form}

    return render(request, 'core/profile_create.html', context)


@login_required(login_url='account_login')
def watch(request, profile_id, *args, **kwargs):
    try:
        profile = Profile.objects.get(uuid=profile_id)
        movies = Movie.objects.filter(age_limit=profile.age_limit)
        movies_trend = movies.order_by('-trend')[:20]
        try:
            showcase = movies[0]
        except:
            showcase = None
        
        if profile not in request.user.profiles.all():
            return redirect('createProfile')
        context = {'movies': movies, 'show_case': showcase, 'profile_id': profile_id, 'movies_trend': movies_trend}
        return render(request, 'core/movie_list.html', context)
        
    except Profile.DoesNotExist:
        return redirect('home')


def api_movie(request, profile_id, *args, **kwargs):
    profile = Profile.objects.get(uuid=profile_id)
    movies = Movie.objects.filter(age_limit=profile.age_limit)
    data = list(movies.values())
    return JsonResponse(data, safe=False)

@login_required(login_url='account_login')
def show_movie_detail(request, movie_id, *args, **kwargs):
    try:
        movie = Movie.objects.get(uuid=movie_id)
        return render(request, 'core/show_movie_detail.html', {'movie': movie})
    except Movie.DoesNotExist:
        return redirect('listProfile')


@login_required(login_url='account_login')
def show_movie(request, movie_id):
    movie = Movie.objects.get(uuid=movie_id)
    movie.trend += 1
    movie.save()
    movie = movie.videos.values()
    return render(request, 'core/show_movie.html', {'movie': list(movie)})
