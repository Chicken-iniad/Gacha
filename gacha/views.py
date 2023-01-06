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

    c_monsters = Monster.objects.filter(user=user).filter(rarity="C").order_by('monsters')
    r_monsters = Monster.objects.filter(user=user).filter(rarity="R").order_by('monsters')
    sr_monsters = Monster.objects.filter(user=user).filter(rarity="SR").order_by('monsters')
    ssr_monsters = Monster.objects.filter(user=user).filter(rarity="SSR").order_by('monsters')
    
    total_get_kind=len(Monster.objects.filter(user=user).values_list('monsters', flat=True).order_by('monsters').distinct())
    all_kind = sum(os.path.isfile(os.path.join("gacha/static/gacha/img/C/", name)) for name in os.listdir("gacha/static/gacha/img/C/")) + sum(os.path.isfile(os.path.join("gacha/static/gacha/img/R/", name)) for name in os.listdir("gacha/static/gacha/img/R/")) + sum(os.path.isfile(os.path.join("gacha/static/gacha/img/SR/", name)) for name in os.listdir("gacha/static/gacha/img/SR/")) + sum(os.path.isfile(os.path.join("gacha/static/gacha/img/SSR/", name)) for name in os.listdir("gacha/static/gacha/img/SSR/"))
    complete_per = int((total_get_kind/all_kind)*100)
    params = {
        'user': user,
        'c_monsters': c_monsters,
        'r_monsters': r_monsters,
        'sr_monsters': sr_monsters,
        'ssr_monsters': ssr_monsters,
        'total_get_kind': total_get_kind,
        'all_kind': all_kind,
        'complete_per': complete_per

    }
    
    return render(request, 'gacha/user.html', params)

@login_required
def select_image(request):
    lst = ["SSR"]+["SR"]*9+["R"]*30+["C"]*60
    rarity = random.choice(lst)
    dir = "gacha/static/gacha/img/"+rarity+"/"
    imgnum = random.randint(1, sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir)))
    # imgpath <- 取得したモンスターの画像のパス
    imgpath = "gacha/img/"+rarity+"/" + str(imgnum) + ".png"
    #現在のユーザーのモンスターリストに取得したモンスターを追加
    monster = Monster(user=request.user, monsters= imgpath, rarity=rarity)
    monster.save()
    #未実装箇所
    return render(request, 'gacha/select_image.html', {'image_path': imgpath, 'rarity': rarity})
