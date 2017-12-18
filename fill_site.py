import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.utils import timezone
from news.models import Post, Profile
from django.contrib.auth.models import Group, User

import random

def fill():
	for i in range(100):
		User1 = add_user(
			username = 'User'+str(i),
			password = 'QazWsxEdc1',
			email = str(i) + '@b.ru',
			)
		Post1 = add_post(
			title = 'Статья №'+str(i),
			text = 'Simple text',
			created_date = timezone.now(),
			published_date = timezone.now(),
			author = User1,
			)

def add_user(username, email, password):
	c = User.objects.get_or_create(
		username = username,
		email = email,
		password = password,
		)[0]
	c.save()
	return c

def add_post(title, text, created_date, published_date, author):
	q = Post.objects.get_or_create(
		title = title,
		text = text,
		created_date = timezone.now(),
		published_date = timezone.now(),
		author = author
		)[0]
	q.save()
	return q

	
if __name__ == '__main__':
	print('starting site fill script')
	fill()
	for user in Profile.objects.all() :
		user.rate = random.randint(1400, 2600)/2
		user.save()
		
	
	
	
	

