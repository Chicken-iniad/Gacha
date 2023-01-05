from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import glob
import os
from .models import Monster
# Create your views here.

def index(request):
    return render(request, 'gacha/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/')
    else:
        form = SignupForm()

    param = {
        'form': form
    }

    return render(request, 'gacha/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                if next == 'None':
                    return redirect(to='/user/')
                else:
                    return redirect(to=next)
    else:
        form = LoginForm()
        next = request.GET.get('next')

    param = {
        'form': form,
        'next': next
    }

    return render(request, 'gacha/login.html', param)

def logout_view(request):
    logout(request)

    return render(request, 'gacha/logout.html')

@login_required
def user_view(request):
    user = request.user

    # monstersは文字列なので、リストに変換する必要がある

    monsters = Monster.objects.filter(user=user)
    params = {
        'user': user,
        'monsters': monsters
    }
    
    return render(request, 'gacha/user.html', params)


def select_image(request):
    lst = ["SSR"]+["SR"]*9+["R"]*30+["C"]*60
    rarity = random.choice(lst)
    dir = "gacha/static/gacha/img/"+rarity+"/"
    imgnum = random.randint(1, sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir)))
    # imgpath <- 取得したモンスターの画像のパス
    imgpath = "gacha/img/"+rarity+"/" + str(imgnum) + ".png"
    #現在のユーザーのモンスターリストに取得したモンスターを追加
    monster = Monster(user=request.user, monsters= imgpath)
    monster.save()
    #未実装箇所
    return render(request, 'gacha/select_image.html', {'image_path': imgpath, 'rarity': rarity})
