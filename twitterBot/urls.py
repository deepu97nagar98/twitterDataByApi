"""twitterBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
from tweetapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^auth/$', views.auth, name='oauth_auth'), 
    url(r'^callback/$', views.callback, name='auth_return'),
    url(r'^home/$', views.home, name='home'), 
    url(r'^unauth/$', views.unauth, name='unauth'),
    url(r'^tweetsoffriends/$', views.tweetsoffriends, name='tweetsoffriends'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^tweetRetweetbyfriends/$', views.tweetRetweetbyfriends, name='tweetRetweetbyfriends'),
    url(r'^likeRetweetByTweetText/$', views.likeRetweetByTweetText, name='likeRetweetByTweetText'),
]
