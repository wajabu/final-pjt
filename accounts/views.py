from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from .forms import FondForm


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('community:index')

# profile 여기다가 영화 장르 정보, 영화 포스터 정보 전달
@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                isFollowed = False
            else:
                person.followers.add(user)
                isFollowed = True
            context = {
                'isFollowed':isFollowed,
                'following_count': person.followings.count(),
                'followers_count': person.followers.count()
            }
            return JsonResponse(context)
        return redirect('accounts:profile', person.username)
    return render(request, 'accounts/login.html')


# create 취향
# 좋아하는 장르, 싫어하는 장르, 좋아하는 영화 선택
@require_http_methods(['GET', 'POST'])
def fond_create(request, username):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), username=username)
        if request.method == 'POST':
            form = FondForm(request.POST) 
            if form.is_valid():
                person = form.save(commit=False)
                person.user = request.user
                person.save()
                return redirect('accounts:profile', username)
        else:
            form = FondForm()
        context = {
            'form': form,
            'username': username,
            'person':person,
        }
        return render(request, 'accounts/fond_create.html', context)
    return redirect('accounts:profile', username)


# update 취향

# delete 취향

