from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect, Http404 
from django.contrib.auth.forms import UserCreationForm 
from django.core.context_processors import csrf
from django.contrib.auth.models import User

        

def register(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect('/accounts/register/complete')

     else:
         form = UserCreationForm()
     token = {}
     token.update(csrf(request))
     token['form'] = form

     return render_to_response('registration/register.html', token)

 def registration_complete(request):
     return render_to_response('registration/registration_complete.html')
     