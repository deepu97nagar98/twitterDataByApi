import tweepy

#Application key
CONSUMER_KEY = '6mqIn8qoITteWQToleXVKoS1k'
CONSUMER_SECRET = '3n8d2C1ojYcEWbDt3kKC0F8Dvj8Iq8iHhm9XZz4mznFj6VKGKA'

def get_api(request):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth,wait_on_rate_limit=True)
	return api
