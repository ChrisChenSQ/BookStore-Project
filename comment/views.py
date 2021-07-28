from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from index.models import *
from user.models import *
from django.db.models import Sum, Count

import time


def commentView(request, book_id):
    # search info
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    # request is post
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        numrate = request.POST.get('numrating', '')
        comment_user = request.user.username

        # button top n
        top = request.POST.get('top', '')
        kint = request.POST.get('kint', '5')
        if top:
            print('click on button', top, kint)
            newkint = int(kint)
            book_info = Book.objects.filter(book_id=book_id).first()
            #
            if not book_info:
                raise Http404
            comment_all = Comment.objects.filter(book_id=book_id).order_by('-comment_tmp')[:newkint]
            book_name = book_info.book_name
            book_rate = book_info.book_numrating
            page = int(request.GET.get('page', 1))
            paginator = Paginator(comment_all, 5)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            return render(request, 'comment.html', locals())
        print("the comment is {} the numbner is  {}".format(comment_text, numrate))

        # comment already
        comment_info = Comment.objects.filter(comment_user=comment_user).filter(book_id=book_id)
        if comment_info:
            return redirect('/comment/%s.hhtml' % (str(book_id)))

        if numrate:
            book_info = Book.objects.filter(book_id=book_id).first()
            book_info.book_numrating += 1
            book_info.book_numtext += 1
            book_info.book_avg_rating = (book_info.book_avg_rating * book_info.book_numrating + int(numrate)) / (
                        book_info.book_numrating + 1)
            book_info.save()

        comment_user = request.user.username if request.user.username else 'anonymous user'
        if comment_text:
            comment = Comment()
            comment.comment_text = comment_text
            comment.comment_user = comment_user
            comment.comment_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            comment.book_id = book_id
            comment.save()
        return redirect('/comment/%s.html' % (str(book_id)))
    else:
        book_info = Book.objects.filter(book_id=book_id).first()
        # book execption
        if not book_info:
            raise Http404
        comment_all = Comment.objects.filter(book_id=book_id).order_by('comment_date')
        book_name = book_info.book_name
        book_rate = book_info.book_avg_rating

        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'comment.html', locals())


# the function that if the user have already comment the book, then we render this page.
def already_commentView(request, book_id):
    # search info
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    # request is post
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        numrate = request.POST.get('numrating', '')
        comment_user = request.user.username

        # button top n
        top = request.POST.get('top', '')
        kint = request.POST.get('kint', '5')
        if top:
            print('click on button', top, kint)
            newkint = int(kint)
            book_info = Book.objects.filter(book_id=book_id).first()
            #
            if not book_info:
                raise Http404
            comment_all = Comment.objects.filter(book_id=book_id).order_by('-comment_tmp')[:newkint]
            book_name = book_info.book_name
            book_rate = book_info.book_numrating
            page = int(request.GET.get('page', 1))
            paginator = Paginator(comment_all, 5)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            return render(request, 'comment.html', locals())
        print("the comment is {} the numbner is  {}".format(comment_text, numrate))

        # comment already
        comment_info = Comment.objects.filter(comment_user=comment_user).filter(book_id=book_id)
        if comment_info:
            return redirect('/comment/%s.hhtml' % (str(book_id)))

        if numrate:
            book_info = Book.objects.filter(book_id=book_id).first()
            newnum = book_info.book_numrating
            newnum = newnum + int(numrate)
            Book.objects.filter(book_id=book_id).update(book_numrating=newnum)

        comment_user = request.user.username if request.user.username else 'anonymous user'
        if comment_text:
            comment = Comment()
            comment.comment_text = comment_text
            comment.comment_user = comment_user
            comment.comment_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            comment.book_id = book_id
            comment.save()
        return redirect('/comment/%s.html' % (str(book_id)))
    else:
        book_info = Book.objects.filter(book_id=book_id).first()
        # book execption
        if not book_info:
            raise Http404
        comment_all = Comment.objects.filter(book_id=book_id).order_by('comment_date')
        book_name = book_info.book_name
        book_rate = book_info.book_numrating

        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'alreadycomment.html', locals())


# see the user detail function
def commentView1(request, commentuser, book_id):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    print('view1 user is ', commentuser)
    print('new bookidis ', book_id)
    book_info = Book.objects.get(book_id=int(book_id))

    # commentuser=commentuser
    comment_all = Comment.objects.filter(comment_user=commentuser).order_by('comment_date')
    user_info = MyUser.objects.filter(username=commentuser).first()
    # user1=user_info[0].username
    # score1=user_info[0].score
    # book_name = book_info.book_name
    # print('user is ',user_info[0].id,score1)
    # print('bookinfo',book_info[0].book_name)
    page = int(request.GET.get('page', 1))
    paginator = Paginator(comment_all, 2)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    #  return HttpResponse('dislike')
    return render(request, 'comment1.html', locals())


# disscore function
def commentView2(request, commentuser, book_id):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    print('view2 user is ', commentuser, book_id)
    book_info = Book.objects.get(book_id=int(book_id))
    print('end book_info')
    myuser = MyUser.objects.filter(username=commentuser).first()
    print('before score is ', myuser.score)
    myuser.disscore = myuser.disscore + 1
    myuser.scoregap = myuser.scoregap - 1

    print('score is ', myuser.disscore, myuser.scoregap)
    myuser.save()
    user_info = MyUser.objects.filter(username=commentuser).first()
    comment_all = Comment.objects.filter(comment_user=commentuser).order_by('comment_date')
    book_info = Book.objects.get(book_id=int(book_id))
    page = int(request.GET.get('page', 1))
    paginator = Paginator(comment_all, 2)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    #    return HttpResponse('dislike')
    return render(request, 'comment1.html', locals())


# user1 lable user2 as trust user function
def commentView3(request, commentuser, book_id):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]

    print('view2 user is ', commentuser, book_id)
    book_info = Book.objects.get(book_id=int(book_id))
    print('end book_info')
    myuser = MyUser.objects.filter(username=commentuser).first()
    print('before score is ', myuser.score)
    myuser.score = myuser.score + 1
    myuser.scoregap = myuser.scoregap + 1
    print('score is ', myuser.score, myuser.scoregap)
    myuser.save()

    relation = Userrela()
    relation.userrela_userid1 = request.user.username
    relation.userrela_userid2 = commentuser
    relation.userrela_relation = 1
    relation.save()

    user_info = MyUser.objects.filter(username=commentuser).first()
    comment_all = Comment.objects.filter(comment_user=commentuser).order_by('comment_date')
    book_info = Book.objects.get(book_id=int(book_id))
    page = int(request.GET.get('page', 1))
    paginator = Paginator(comment_all, 2)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    #    return HttpResponse('dislike')
    return render(request, 'comment1.html', locals())


# edit own's comment score; add score to other user's comment
def addscore(request, comment_id, book_id):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    if request.method == 'POST':
        book_info = Book.objects.filter(book_id=book_id).first()
        # get book information  
        if not book_info:
            raise Http404
        comment_text = request.POST.get('comment', '')
        numrate = request.POST.get('numrating', '0')
        pid = Comment.objects.filter(comment_id=comment_id).first()
        my_user = MyUser.objects.filter(username=pid.comment_user).first()
        comment_user = request.user.username
        # numrate=int(numrate)
        numrate = int(numrate)
        comment_user = request.user.username if request.user.username else 'Unkonw User'
        if numrate:
            if pid.comment_rate == 0:
                pid.comment_rate = int(numrate)
                pid.comment_tmp += 1
            else:
                pid.comment_rate = round((int(numrate) + pid.comment_rate * pid.comment_tmp)/ (pid.comment_tmp+1),2)
                pid.comment_tmp += 1
            pid.save()
            my_user.sumcomment += numrate
            my_user.save()
        # edit own's comment
        if comment_user == pid.comment_user:
            Comment.objects.filter(comment_id=comment_id).update(comment_text=comment_text)
        comment_all = Comment.objects.filter(comment_id=comment_id)
        book_name = book_info.book_name
        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        if comment_user == comment_all[0].comment_user:
            return render(request, 'commentupdate.html', locals())

        return render(request, 'commentscore.html', locals())
        # return redirect('/comment/%s.html' %(str(book_id)))
    else:
        book_info = Book.objects.filter(book_id=book_id).first()
        if not book_info:
            raise Http404
        comment_all = Comment.objects.filter(comment_id=comment_id)
        comment_user = request.user.username
        book_name = book_info.book_name
        print('user is ', comment_user, comment_all[0].comment_user)

        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        print('user is ', comment_user, comment_all[0].comment_user)
        if comment_user == comment_all[0].comment_user:
            print('I am in ')
            return render(request, 'commentupdate.html', locals())

        return render(request, 'commentscore.html', locals())

# useless function
def updatescore(request, comment_id, book_id):
    search_book = Dynamic.objects.select_related('book').order_by('-dynamic_search').all()[:6]
    if request.method == 'POST':
        book_info = Book.objects.filter(book_id=book_id).first()
        # get book information
        if not book_info:
            raise Http404
        comment_text = request.POST.get('comment', '')
        numrate = request.POST.get('numrating', '')
        pid = Comment.objects.filter(comment_id=comment_id).first()
        print('I in update post score')
        comment_user = request.user.username if request.user.username else 'Unknow User'
        if numrate:
            if pid.comment_rate == 0:
                pid.comment_rate = int(numrate)
                pid.comment_tmp += 1
            else:
                pid.comment_tmp += 1
                pid.comment_rate = (int(numrate) + pid.comment_rate * pid.comment_tmp)/pid.comment_tmp
            pid.save()
        comment_all = Comment.objects.filter(comment_id=comment_id)
        book_name = book_info.book_name
        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'commentscore.html', locals())
        # return redirect('/comment/%s.html' %(str(book_id)))
    else:
        book_info = Book.objects.filter(book_id=book_id).first()
        if not book_info:
            raise Http404
        comment_all = Comment.objects.filter(comment_id=comment_id)
        print('I in update score')
        comment_user = request.user.username
        book_name = book_info.book_name
        print('user is ', comment_user, comment_all[0].comment_user)

        page = int(request.GET.get('page', 1))
        paginator = Paginator(comment_all, 5)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        print('user is ', comment_user, comment_all[0].comment_user)
        if (comment_user == comment_all[0].comment_user):
            print('I am in ')
            return render(request, 'commentupdate.html', locals())

        return render(request, 'commentscore.html', locals())
