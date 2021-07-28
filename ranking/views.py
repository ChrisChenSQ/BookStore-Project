from django.shortcuts import render
from index.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse

def rankingView(request):
  #if request.method == 'GET':

    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:4]

    All_list = Book.objects.values('book_type').distinct()

    book_type = request.GET.get('type', '')
   # page = request.GET.get('page')

    #print('ranking first',page)
    print('ranking no page')
    username=request.user.username
    print('ranking username is ',username)
    if book_type:
        book_info = Book.objects.filter(book_type=book_type)
    else:
        book_info = Book.objects.filter(~Q(book_bookstock=0))
  
    #paginator = Paginator(book_info, 5)
    #try:
    #    contacts = paginator.page(page)
    #except PageNotAnInteger:
    #        contacts = paginator.page(1)
    #except EmptyPage:
    #        contacts = paginator.page(paginator.num_pages)
    return render(request, 'ranking.html', locals())
 



from django.views.generic import ListView
class RankingList(ListView):

    context_object_name = 'book_info'

    template_name = 'ranking.html'

    def get_queryset(self):

        book_type = self.request.GET.get('type', '')
        if book_type:
            book_info = Dynamic.objects.select_related('book').filter(book__book_type=book_type).order_by('-dynamic_plays').all()[:10]
        else:
            book_info = Dynamic.objects.select_related('book').order_by('-dynamic_plays').all()[:10]
        return book_info


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_book'] = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:4]

        context['All_list'] = Book.objects.values('book_type').distinct()
        return context

def rankingView1(request,page):
  if request.method == 'GET':

    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:4]

    All_list = Book.objects.values('book_type').distinct()

    book_type = request.GET.get('type', '')
   # page = request.GET.get('page')

    print('ranking page is',page)
    print('ranking  page')
    if book_type:
        book_info = Dynamic.objects.select_related('book').filter(book__book_type=book_type).order_by('-dynamic_plays').all()[:10]
    else:
        book_info = Dynamic.objects.select_related('book').order_by('-dynamic_plays').all()[:20]

    paginator = Paginator(book_info, 5)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
            contacts = paginator.page(1)
    except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
    return render(request, 'ranking1.html', locals())


