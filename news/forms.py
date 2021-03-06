from django import forms

from .models import Post, Profile, Game, Player
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('vk_page',)

class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ('title', 'maxPlayers')

	