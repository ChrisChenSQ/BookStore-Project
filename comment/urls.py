"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('<int:book_id>.html', views.commentView, name='comment'),
    path('<int:book_id>.hhtml', views.already_commentView, name = "havecomment"),
    path('<int:comment_id>and<int:book_id>.dhtml', views.addscore, name='commentscore'),
    path('<int:comment_id>and<int:book_id>.ddhtml', views.updatescore, name='commentupdate'),
    path('<slug:commentuser>and<int:book_id>.hhtml', views.commentView1, name='comment1'),
    path('<slug:commentuser>and<int:book_id>.minushtml', views.commentView2, name='comment2'),
    path('<slug:commentuser>and<int:book_id>.addhtml', views.commentView3, name='comment3'),
]
