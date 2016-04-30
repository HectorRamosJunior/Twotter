from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import TwotterProfile, Twoot
from .forms import UserForm, TwotterProfileForm, TwootForm

import json


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        twotter_profile = User.objects.get(username=request.user.username).twotter_profile
        twoots = Twoot.objects.all().order_by('-creation_date')
    else:
        twotter_profile = None
        twoots = Twoot.objects.all()

    context = {'twotter_profile': twotter_profile, 'twoots': twoots}

    return render(request, 'twotter/index.html', context)

def redirect_to_index(request):
    return redirect('/twotter/')

def twotter_profile(request, username):
    return redirect('/twotter/')

@login_required
def make_twoot(request):
    if request.method == "POST":
        print "Here's the text", request.POST.get("twoot_text")
        twoot_form = TwootForm({"text": request.POST.get("twoot_text")})

        if twoot_form.is_valid():
            twoot = twoot_form.save(commit=False)
            twoot.twotter_profile = request.user.twotter_profile
            twoot.save()

            return HttpResponse(json.dumps(""), content_type="application/json")
        else:
            print twoot_form.errors
    else:
        return redirect('/twotter/')


def user_login_or_register(request):
    # First time visining page, present login forms
    if request.method == "GET":
        user_form = UserForm()
        twotter_profile_form = TwotterProfileForm()
        context = {'user_form': user_form, 'twotter_profile_form': twotter_profile_form}

        return render(request, 'twotter/login.html', context)
    elif request.method == "POST":
        if request.POST["button"] == "Login":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:    # Verify user is not banned
                    login(request, user)
                    return redirect('/twotter/')
            else:
                error = "Account or Password provided was incorrect."
                context = {'user_form': UserForm(), 'twotter_profile_form': TwotterProfileForm(), 'error': error}

                return render(request, 'twotter/login.html', context)
        elif request.POST["button"] == "Register":
            registered = False
            error = None

            user_form = UserForm(data=request.POST)
            twotter_profile_form = TwotterProfileForm(data=request.POST)

            if user_form.is_valid() and twotter_profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                twotter_profile = twotter_profile_form.save(commit=False)
                twotter_profile.user = user
                if twotter_profile.avatar_url == "":
                    twotter_profile.avatar_url = "http://i.imgur.com/3iMO8An.png"
                if twotter_profile.background_url == "":
                    twotter_profile.background_url = ""
                twotter_profile.save()

                registered = True

                # Authenticate and login!
                new_user = authenticate(
                                            username=user_form.cleaned_data['username'],
                                            password=user_form.cleaned_data['password'],
                                        )
                login(request, new_user)
            # Handle form errors
            else:
                error = user_form.errors
                error.update(twotter_profile_form.errors)

            context = {'user_form': user_form, 'twotter_profile_form': twotter_profile_form,
                    'registered': registered, 'error': error}

            return render(request, 'twotter/login.html', context)

@login_required
def user_logout(request):
    logout(request)

    return redirect('twotter/')