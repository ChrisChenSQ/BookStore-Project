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
    path('<int:book_id>.html', views.CartView, name='order'),
    path('<int:cart_id>and<int:book_id>carthtml', views.CartViewminus, name='orderminus'),
    path('<int:cart_id>and<int:book_id>addhtml', views.CartViewadd, name='orderadd'),
    path('<int:cart_id>and<int:book_id>delhtml', views.CartViewdelete, name='orderdelete'),
    path('ordercommit.html', views.CartViewplace, name='orderplace'),
    path('<int:book_id>.ahtml', views.orderView4, name='order4'),
    path('recommend.html', views.recommendView, name='order1'),
    path('confirmorder.html', views.confirmorder, name = 'confirmorder'),
]
