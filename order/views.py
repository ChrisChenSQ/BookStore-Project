from django.shortcuts import HttpResponse, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from index.models import *
import time


# this class is for the shopping cart
def CartView(request, book_id):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        cart_username = request.user.username
        # content of search
        kword = request.session.get('kword', '')
        book = Book.objects.get(book_id=book_id)
        try_cart = Cart.objects.filter(cart_username=cart_username, status=1)
        # determine whether the book is already in the shopping cart
        for i in try_cart:
            if i.cart_booktitle == book.book_name:
                book_info = Cart.objects.filter(cart_username=cart_username, status=1)
                page = 1
                print('this is in try', page)
                totalsum = 0
                for o in book_info:
                    totalsum += o.total()
                print('already total is ', totalsum)
                return render(request, 'order.html', locals())
        # if the book is not in the shopping cart, then add it into the db and shopping cart.
        cart = Cart()
        cart.cart_username = cart_username
        cart.cart_quantity = 1
        cart.cart_booktitle = book.book_name
        cart.cart_bookid = book.book_id
        cart.cart_bookprice = book.book_price
        cart.cart_publisher = book.book_publisher
        cart.cart_bookrate = book.book_avg_rating
        cart.cart_auther = book.book_author
        cart.status = 1
        cart.save()
        orders = Cart.objects.filter(cart_username=cart_username)
        book_info = Cart.objects.filter(cart_username=cart_username, status=1)
        totalsum = 0
        for o in book_info:
            totalsum += o.total()
        print('total price is ', totalsum)
        page = 1
        return render(request, 'order.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')


def CartViewminus(request, cart_id, book_id):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        cart_username = request.user.username

        # minus quantity of the shopping cart
        cartnum = Cart.objects.filter(cart_id=cart_id)
        newnum = int(cartnum[0].cart_quantity) - 1
        Cart.objects.filter(cart_id=cart_id).update(cart_quantity=newnum)
        book_info = Cart.objects.filter(cart_username=cart_username, status=1)
        orders = Cart.objects.filter(cart_username=cart_username)
        # calcu total of all books
        totalsum = 0
        for o in book_info:
            totalsum += o.total()
        page = 1
        print('minus is ', totalsum)
        return render(request, 'order.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')


def CartViewadd(request, cart_id, book_id):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        cart_username = request.user.username

        # add quantity of the shopping cart
        cartnum = Cart.objects.filter(cart_id=cart_id)
        newnum = int(cartnum[0].cart_quantity) + 1
        Cart.objects.filter(cart_id=cart_id).update(cart_quantity=newnum)
        book_info = Cart.objects.filter(cart_username=cart_username, status=1)
        orders = Cart.objects.filter(cart_username=cart_username)
        # calcu total of all books
        totalsum = 0
        for o in book_info:
            totalsum += o.total()
        page = 1
        print('minus is ', totalsum)
        return render(request, 'order.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')


def CartViewdelete(request, cart_id, book_id):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        cart_username = request.user.username

        Cart.objects.get(cart_id=cart_id).delete()
        book_info = Cart.objects.filter(cart_username=cart_username, status=1)
        # calcu total of all books
        totalsum = 0
        for o in book_info:
            totalsum += o.total()
        page = 1
        return render(request, 'order.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')


def CartViewplace(request):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        cart_username = request.user.username
        # insert data to index_order,index_orderinfo
        last_order = Order.objects.last()
        new_orderid = last_order.order_id + 1
        order = Order()
        order.order_id = new_orderid
        order.order_userid = cart_username
        order.order_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        order.price = 11
        order.save()

        book_info = Cart.objects.filter(cart_username=cart_username, status=1)
        orderinfo = Orderinfo()
        book = Book()
        last_num = Orderinfo.objects.last()
        num = last_num.id
        dynamic = Dynamic()

        print('hihi', num)
        for o in book_info:
            num += 1
            print('into o', o.cart_auther, num)
            orderinfo.order_id = new_orderid
            orderinfo.order_auther = o.cart_auther
            orderinfo.order_name = cart_username
            orderinfo.order_bookqua = o.cart_quantity
            orderinfo.order_publisher = o.cart_publisher
            orderinfo.order_bookprice = o.cart_bookprice
            orderinfo.order_bookrate = o.cart_bookrate
            orderinfo.order_booktitle = o.cart_booktitle
            orderinfo.order_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            orderinfo.id = num
            orderinfo.save()
            add_book = Book.objects.filter(book_name=o.cart_booktitle).first()
            add_book.book_saleamount += 1
            add_book.save()
            dy = Dynamic.objects.filter(book_id=add_book.book_id).first()
            dy.dynamic_down += 1
            dy.save()

        Cart.objects.filter(cart_username=cart_username).update(status=0)
        # print('after update',book_info[0].status)
        # calcu total of all books
        totalsum = 0
        for o in book_info:
            totalsum += o.total()
        page = 1
        return render(request, 'ordercommit.html', locals())
    else:
        # request is post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect('/order/1.html')


# recommend function
def recommendView(request):
    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        book_info = Book.objects.order_by('book_saleamount')[:5]
        book_rate_info = Book.objects.order_by('book_avg_rating')[:5]
        order = Orderinfo.objects.all()

        # get all the order infroamtion of all the user
        order_info = []
        for i in order:
            if order_info == []:
                order_info.append([i.order_booktitle])
            elif i.order_id > len(order_info):
                order_info.append([i.order_booktitle])
            elif i.order_id == len(order_info):
                order_info[i.order_id-1].append(i.order_booktitle)

        # get the list of book that the user order
        user_order = Order.objects.filter(order_userid=request.user.username)
        user_order_detial = []
        for i in user_order:
            for book in order_info[i.order_id-1]:
                user_order_detial.append(book)

        #ge the list of book base on other's buying record.
        suggestion = []
        for i in user_order_detial:
            for a in order_info:
                if i in a and len(a) > 1:
                    for b in a:
                        if i != b and b not in user_order_detial:
                            suggestion.append(b)
        suggestion_book = Book.objects.filter(book_name__in=suggestion)
        if suggestion == []:
            return render(request, 'recommend.html', locals())
        else:
            return render(request, 'recommand_withotheruser.html', locals())



# this class is for direct order
def orderView4(request, book_id):
    if request.method == 'POST':
        kint = request.POST.get('kint', '')
        if kint != "":
            book_info = Book.objects.get(book_id=int(book_id))
            book_price = book_info.book_price
            total = int(kint) * int(book_price)
            name = request.user.username
            last_order = Order.objects.last()
            new_orderid = last_order.order_id + 1
            order = Order()
            orderinfo = Orderinfo()
            book = Book()
            order.order_id = new_orderid
            order.order_userid = name
            order.order_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            order.order_price = total
            orderinfo.order_id = new_orderid
            orderinfo.order_auther = book_info.book_author
            orderinfo.order_name = name
            orderinfo.order_bookqua = int(kint)
            orderinfo.order_publisher = book_info.book_publisher
            orderinfo.order_bookprice = book_info.book_price
            orderinfo.order_bookrate = book_info.book_avg_rating
            orderinfo.order_booktitle = book_info.book_name
            orderinfo.order_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            order.save()
            orderinfo.save()
            Book.objects.filter(book_id=book_id).update(book_bookstock=(book_info.book_bookstock - 1))
            return render(request, 'order5.html', locals())

    if request.method == 'GET':
        # search book
        search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
        # distinct of type book
        All_list = Book.objects.values('book_type').distinct()
        # type of book
        # song_type = request.GET.get('type', '')
        book_info = Book.objects.get(book_id=int(book_id))
        name = request.user.username
        kint = request.session.get('kint', '')
        print('show variable book_id name,qua', book_id, name, kint)
        return render(request, 'order4.html', locals())

        # return HttpResponse("Succeed in database")
    else:
        # request is post
        request.session['kword'] = request.POST.get('kint', '')
        p = request.POST.get('kint', '')
        print('post other', p)
        return redirect('/order/1.html')


def confirmorder(request):
    # total=request.Post.get('quantity')
    total = request.GET.get('quantity')
    totaltext = request.GET.get('name')
    print('quantity is ', total, totaltext)
    return render(request, "confirmorder.html", locals())
