from django.utils import timezone
from .models import Post, Profile, Game, Player
from .forms import PostForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, loader
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from news.forms import UserForm, ProfileForm, GameForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model

import random

User = get_user_model()

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'news/post_list.html', {'posts': posts})

def rate_list(request):
	rates = Profile.objects.order_by('-rate')
	return render(request, 'news/rating.html', {'rates':rates})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'news/post_detail.html', {'post': post})

def rules(request):
    return render(request, 'news/rules.html')

def index(request):
	games = Game.objects.order_by('maxPlayers')
	return render(request, 'news/index.html', {'games': games})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'news/post_edit.html', {'form': form})

@login_required
def game_new(request):
    if request.method == "POST":
        game = GameForm(request.POST)
        if game.is_valid():
            game = game.save(commit=False)
            game.author = request.user
            game.save()
            return redirect('index')
    else:
        game = GameForm()
    return render(request, 'news/new_game.html', {'game': game})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'news/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'news/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def game_remove(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return redirect('index')

@login_required
def game_playing(request, pk):
    game = get_object_or_404(Game, pk=pk)
    players = game.Player.objects.all()
    for player in players:
    	player.user.profile.rate = player.user.profile.rate + random.randint(-20, 20)/2
    game.delete()
    return redirect('index')

@login_required
@transaction.atomic    
def profile_detail(request):
    try:
        user = User.objects.select_related('profile').get(id = request.user.id)
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render (
        request, 'profile/profile_detail.html', {
            'user' : user,
            'user_form': user_form,
            'profile_form': profile_form
        }    
    )

def add_player(request, pk):
	game = get_object_or_404(Game, pk=pk)
	obj_type = ContentType.objects.get_for_model(game)
	player, is_created = Player.objects.get_or_create(
		content_type=obj_type, object_id=game.id, user=request.user)
	#return redirect(player, 'index', {'player' : player})
	return redirect('index')

def remove_player(obj, user):
	obj_type = ContentType.objects.get_for_model(obj)
	Player.objects.filter(
		content_type=obj_type, object_id=obj.id, user=user
		).delete()

def is_fan(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    players = Player.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()

def get_fans(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        players__content_type=obj_type, players__object_id=obj.id)
