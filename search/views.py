from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from index.models import *
def searchView(request, page):
    if request.method == 'GET':
        # search book 
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        # conent of book ,kword is null,mean searching full book 
        kword = request.session.get('kword', '')
        #order_auther=request.user.username
        #order=Order()
        #order.order_auther=order_auther
        #order.save()
        if kword:
            # Q is or of sql
            book_info = Book.objects.filter(Q(book_name__icontains=kword) | Q(book_author=kword)| Q(book_publisher=kword)| Q(book_language=kword)).all()
        else:
            book_info = Book.objects.all()
        #page function
        paginator = Paginator(book_info, 10)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        #record  
        book_exist = Book.objects.filter(book_name=kword)
        if book_exist:
            book_id = book_exist[0].book_id
            dynamic_info = Dynamic.objects.filter(book_id=int(book_id)).first()
            # record of dynamic 
            if dynamic_info:
                dynamic_info.dynamic_search += 1
                dynamic_info.save()
            # new record of dynamic
            else:
                dynamic = Dynamic(dynamic_plays=0, dynamic_search=1, dynamic_down=0, book_id=book_id)
                dynamic.save()
        print('in search get',kword)
        return render(request, 'search.html', locals())
    else:
       # request is post 
        request.session['kword'] = request.POST.get('kword', '')
        #print('second in ',kword)
        return redirect('/search/1.html')

def searchRate(request, page):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        # conent of book ,kword is null,mean searching full book
        kword = request.session.get('kword', '')
        #order_auther=request.user.username
        #order=Order()
        #order.order_auther=order_auther
        #order.save()
        if kword:
            # Q is or of sql
            book_info = Book.objects.filter(Q(book_name__icontains=kword) | Q(book_author=kword)| Q(book_publisher=kword)| Q(book_language=kword)).order_by('-book_avg_rating').all()
        else:
            book_info = Book.objects.order_by('-book_avg_rating').all()
        #page function
        paginator = Paginator(book_info, 10)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        #record of dynamic
        book_exist = Book.objects.filter(book_name=kword)
        if book_exist:
            book_id = book_exist[0].book_id
            dynamic_info = Dynamic.objects.filter(book_id=int(book_id)).first()
            #record
            if dynamic_info:
                dynamic_info.dynamic_search += 1
                dynamic_info.save()
            # new record of dynamic
            else:
                dynamic = Dynamic(dynamic_plays=0, dynamic_search=1, dynamic_down=0, book_id=book_id)
                dynamic.save()
        print('in search get',kword)
        return render(request, 'search1.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        #print('second in ',kword)
        return redirect('/search/1.html')

def searchDate(request, page):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        # conent of book ,kword is null,mean searching full book
        kword = request.session.get('kword', '')
        #order_auther=request.user.username
        #order=Order()
        #order.order_auther=order_auther
        #order.save()
        if kword:
            # Q is or of sql
            book_info = Book.objects.filter(Q(book_name__icontains=kword) | Q(book_author=kword)| Q(book_publisher=kword)| Q(book_language=kword)).order_by('-book_pubdate').all()
        else:
            book_info = Book.objects.order_by('-book_pubdate').all()
        #page function
        paginator = Paginator(book_info, 10)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        #record of dynamic
        book_exist = Book.objects.filter(book_name=kword)
        if book_exist:
            book_id = book_exist[0].book_id
            dynamic_info = Dynamic.objects.filter(book_id=int(book_id)).first()
            #record
            if dynamic_info:
                dynamic_info.dynamic_search += 1
                dynamic_info.save()
            # new record of dynamic
            else:
                dynamic = Dynamic(dynamic_plays=0, dynamic_search=1, dynamic_down=0, book_id=book_id)
                dynamic.save()
        print('in search get',kword)
        return render(request, 'search2.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        #print('second in ',kword)
        return redirect('/search/1.html')
