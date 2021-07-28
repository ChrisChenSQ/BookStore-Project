from django.shortcuts import render
from django.http import StreamingHttpResponse
from index.models import *

def playView(request, book_id):
    # search book
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    # book info
    book_info = Book.objects.get(book_id=int(book_id))
    #
    #book type
    book_type = Book.objects.values('book_type').get(book_id=book_id)['book_type']
    book_relevant = Dynamic.objects.select_related('book').filter(book__book_type=book_type).order_by('-dynamic_views').all()[:6]
    #
    #dynamic of book
    dynamic_info = Dynamic.objects.filter(book_id=int(book_id)).first()
    # dynamic info
    if dynamic_info:
        dynamic_info.dynamic_views += 1
        dynamic_info.save()
    #
    else:
        dynamic_info = Dynamic(dynamic_views=1, dynamic_search=0, dynamic_down=0, book_id=book_id)
        dynamic_info.save()
    return render(request, 'play.html', locals())

#download 
def downloadView(request, book_id):
    #book info 
    book_info = Book.objects.get(book_id=int(book_id))
    #dynamic
    dynamic_info = Dynamic.objects.filter(book_id=int(book_id)).first()
    #
    print('test',request.user.username,book_id)
    #book_author=request.user.username
    #book=Book()
    #book.book_singer=book_singer
    #book.label_id=8
    #book.save()
    if dynamic_info:
        dynamic_info.dynamic_down += 1
        dynamic_info.save()
    # no exist of dynamic 
    else:
        dynamic_info = Dynamic(dynamic_views=0,dynamic_search=0,dynamic_down=1,book_id=book_id)
        dynamic_info.save()
    #
    return response
