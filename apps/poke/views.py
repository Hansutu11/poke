# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Friend, User



# Create your views here.
def index(request):

    return render(request, "poke/index.html")

def login_view(request):
    return render(request, 'poke/login.html')

def register_view(request):
    return render(request, 'poke/register.html')

def login(request):
    result = Friend.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/login_view')
    request.session['id'] = result.id
    return redirect('/dashboard')

def register(request):
    result = Friend.objects.validate_registration(request.POST)
    # print result, type(result)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/register_view')
    request.session['id'] = result.id
    return redirect('/register_view')

def logout(request):
    del request.session['id']
    return redirect('/')

# REQUIRES LOGIN


def increment(request, user_id):
    poking2 = User.objects.get(id=request.session['user_id'])
    poked2 = User.objects.get(id=user_id)
    Friend.objects.create(poking = poking2, poked = poked2)
    return redirect('/dashboard')

def dashboard(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')

    otherfriends = User.objects.exclude(id=request.session['user_id'])
    otherfriends_poked_you = User.objects.get(id=request.session['user_id']).poketake.all()

    counter = 0
    for count in otherfriends:
        if count.pokeamount.count > 0:
            counter += 1

    context = {
        "welcome": User.objects.get(id = request.session['user_id']),
        "otherfriends": otherfriends.all(),
        "counter": counter,
        "otherfriends_poked_you" : User.objects.get(id=request.session['user_id']).poketake.all()
    }
    return render(request, 'poke/dashboard.html', context)
