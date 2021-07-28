from django.shortcuts import render, redirect
from index.models import *
from user.models import *
from .form import MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum,Count

def loginView(request):
    user = MyUserCreationForm()
    if request.method == 'POST':
        if request.POST.get('loginUser', ''):
            loginUser = request.POST.get('loginUser', '')
            password = request.POST.get('password', '')
            if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                user = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)).first()
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('/user/home/1.html')
                else:
                    tips = 'Password Failed'
            else:
                tips = 'User does not exist'
        else:
            user = MyUserCreationForm(request.POST)
            username=request.POST.get('username')
            if user.is_valid():
                user.save()
                tips = 'Sign up success'
                recommend=Recommend()
                recommend.rec_auther=username
                recommend.rec_type='history'
                recommend.save()
            else:
                if user.errors.get('username',''):
                    tips = user.errors.get('username','sign up failed')
                else:
                    tips = user.errors.get('mobile', 'sign up filed')
    return render(request, 'login.html', locals())

#login in
@login_required(login_url='/user/login.html')
def homeView(request, page):
    # user backupgroud 
    name = request.user.username
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:4]
    object_list =Orderinfo.objects.values('order_booktitle','order_publisher','order_auther').annotate(total=Sum('order_bookqua')).order_by('-total') 
    user_info=MyUser.objects.filter(username=name)
    print('is staff',user_info[0].is_staff)
    staff=user_info[0].is_staff
    if staff :
       print('i enter') 
       return render(request, 'home1.html', locals())
    else:
       object_list=Order.objects.filter(order_userid=name)
       return render(request, 'home.html', locals())

#user logout
def logoutView(request):
    logout(request)
    return redirect('/user/home/1.html')

def orderbypublisher(request):
    name = request.user.username
    object_list =Orderinfo.objects.values('order_publisher').annotate(total=Sum('order_bookqua')).order_by('-total')
    user_info=MyUser.objects.filter(username=name)
    print('is staff',user_info[0].is_staff)
    staff=user_info[0].is_staff
    if staff :
       print('i orderbypublisher enter')
       return render(request, 'orderbypublisher.html', locals())
    else:
       return render(request, 'home.html', locals())

def orderbyauthor(request):
    name = request.user.username
    object_list =Orderinfo.objects.values('order_auther').annotate(total=Sum('order_bookqua')).order_by('-total')
    user_info=MyUser.objects.filter(username=name)
    print('is staff',user_info[0].is_staff)
    staff=user_info[0].is_staff
    if staff :
       print('i orderbypublisher enter')
       return render(request, 'orderbyauthor.html', locals())
    else:
       return render(request, 'home.html', locals())

def orderbyuser(request):
    #get name
    name = request.user.username
    object_list =MyUser.objects.all().order_by('-scoregap')
    user_info=MyUser.objects.filter(username=name)
    print('is staff',user_info[0].is_staff)
    staff=user_info[0].is_staff
    if staff :
       print('i orderbypublisher enter')
       return render(request, 'orderbyuser.html', locals())
    else:
       return render(request, 'home.html', locals())


def orderbyusercomment(request):
    #get name
    name = request.user.username
    object_list =MyUser.objects.all().order_by('-sumcomment')
    user_info=MyUser.objects.filter(username=name)
    print('is staff',user_info[0].is_staff)
    staff=user_info[0].is_staff
    if staff :
       print('i orderbypublisher enter')
       return render(request, 'orderbyusercomment.html', locals())
    else:
       return render(request, 'home.html', locals())
