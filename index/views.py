from django.shortcuts import render, redirect
from .models import *


def indexView(request):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:8]
    label_list = Label.objects.all()
    play_hot_book = Dynamic.objects.select_related('book').order_by('-dynamic_views').all()[:10]
    daily_recommendation = Book.objects.order_by('-book_pubdate').all()[:3]
    search_ranking = search_book[:6]
    down_ranking = Dynamic.objects.select_related('book').order_by('-dynamic_down').all()[:6]
    all_ranking = [search_ranking, down_ranking]
    return render(request, 'index.html', locals())


def degreesearch(request):
    if request.method == 'GET':
        return render(request, 'degree_search.html', locals())
    else:
        author_name = request.POST.get('kword', '')
        degree = Author.objects.filter(author_author1=author_name)

        return render(request, 'degree_search_result.html', locals())


def page_not_found(request):
    return render(request, 'error404.html', status=404)
