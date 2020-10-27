from django.shortcuts import render
from twitterBot import settings
import tweepy
from django.http import *
from django.urls import reverse
from tweetapp.utils import *
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime


def login(request):
	
	if validateSession(request):
		return HttpResponseRedirect(reverse('home')) 
	else:
		return render(request,'login.html')

def validateSession(request):
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True

def auth(request):
	oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
	auth_url = oauth.get_authorization_url(True)
	response = HttpResponseRedirect(auth_url)
	
	request.session['request_token'] = oauth.request_token
	return response

def callback(request):
	verifier = request.GET.get('oauth_verifier')
	oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
	token = request.session.get('request_token')

	request.session.delete('request_token')
	oauth.request_token = token
	try:
		oauth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error, failed to get access token')

	request.session['access_key_tw'] = oauth.access_token
	request.session['access_secret_tw'] = oauth.access_token_secret
	print(request.session['access_key_tw'])
	print(request.session['access_secret_tw'])
	response = HttpResponseRedirect(reverse('home'))
	return response

def home(request):
	if validateSession(request):
		api = get_api(request)
		user = api.me()
		return render(request,'home.html', {'user' : user})
	else:
		return HttpResponseRedirect(reverse('login'))	

def unauth(request):
	if validateSession(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('login'))

@api_view(['GET'])
def tweetsoffriends(request):
	api = get_api(request)
	timeLineInfo=[]
	prev_time=datetime.datetime.now()-datetime.timedelta(days=1)
	print(prev_time)
	for tweet in tweepy.Cursor(api.home_timeline).items(300):
		if tweet.created_at>=prev_time:
			tweetLatest={}
			tweetLatest['tweet']=tweet.text
			tweetLatest['tweetedBy']=tweet.user.name
			tweetLatest['retweet_count']=tweet.retweet_count
			tweetLatest['favorite_count']=tweet.favorite_count
			tweetLatest['created_at']=tweet.created_at
			timeLineInfo.append(tweetLatest)
	return Response(timeLineInfo)

@api_view(['POST'])
def likeRetweetByTweetText(request):
	likeRetweetedOnfo=[]
	try:
		qtweet=request.data['qtweet']
		like=request.data['like']
		retweet=request.data['retweet']
		api = get_api(request)
	#matched tweet Ids 'This can be replaced with search api which allows user to like, retweet any tweet'
		tweetsids={}
		for tweet in tweepy.Cursor(api.home_timeline).items():
			if tweet.text.find(qtweet)!= -1:
				tweetsids[tweet.id]=tweet.text
		likeInfo=[]
		if like:
			for id in tweetsids:
				likes={}
				api.create_favorite(id)
				likes['id']=id
				likes['tweet']=tweetsids[id]
				likes['liked']='true'
				likeInfo.append(likes)
		retweetInfo=[]
		if retweet:
			for id in tweetsids:
				retweets={}
				api.retweet(id)
				retweets['id']=id
				retweets['tweet']=tweetsids[id]
				retweets['retweeted']='true'
				retweetInfo.append(retweets)
		likeRetweetedOnfo=[likeInfo,retweetInfo]
	except:
		likeRetweetedOnfo=[{"success":False}]
	return Response(likeRetweetedOnfo)

@api_view(['POST'])
def tweetRetweetbyfriends(request):
	retweetedInfo=[]
	try:
		api = get_api(request)
		qtweet=request.data['qtweet']
	#find the followings list first
		friends=[]
		for user in tweepy.Cursor(api.friends).items():
			friends.append(user.name)
	#collect matched tweet Id's
		ids=[]
		for tweet in tweepy.Cursor(api.user_timeline).items():
			if tweet.text.find(qtweet)!= -1:
				ids.append(tweet.id)
	#return retweeted info of specific tweet
		print(ids)
		retweets_list=[]
		for id in ids:
			retweets_list= 	api.retweets(id)
		for retweet in retweets_list:
			respdict={}
			if retweet.user.name in friends:
				respdict['retweet_id']=retweet.id
				respdict['tweet']=retweet.text
				respdict['retweetedBy']=retweet.user.name
				retweetedInfo.append(respdict)
	except:
		retweetedInfo=[{"success":False}]	
	return Response(retweetedInfo)

@api_view(['GET'])
def friends(request):
	api = get_api(request)
	friends=[]
	followers=[]
	for user in tweepy.Cursor(api.friends).items():
		friends.append(user.name)
	for user in tweepy.Cursor(api.followers).items():
		followers.append(user.name)
	response={'Followings':friends, 'Followers':followers}
	return Response(response)
