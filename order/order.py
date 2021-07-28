from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from index.models import *
def orderView(request, song_id):
    if request.method == 'GET':
        search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
        kword = request.session.get('kword', '')
        
        order_auther=request.user.username
        order=Order()
        order.order_auther=order_auther
        order.order_text=song_id
        order.order_qua=1
        order.save()
        
        song_info=Order.objects.all

        paginator = Paginator(song_info, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        
        return render(request, 'order.html', locals())
    else:
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')