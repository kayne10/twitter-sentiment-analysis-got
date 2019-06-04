import psycopg2
import json
import os
import tweepy
import time
from dateutil import parser

# Twitter API keys and DB password
# TODO:
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
password = os.environ["password"]


def connect(username, created_at, tweet, retweet_count, place, location):
    """Connect to postgres database and insert data"""
    try:
        conn = psycopg2.connect(host='localhost',database='tweetsdb',user='troy',password=password)
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO tweets (username, created_at, tweet, retweet_count, place, location) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
            conn.commit()
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()
    return


# Tweepy Streamer object
class Streamlistener(tweepy.StreamListener):


	def on_connect(self):
		print("You are connected to the Twitter API")


	def on_error(self):
		if status_code != 200:
			print("error found")
			# returning false disconnects the stream
			return False

	"""
	This method reads in tweet data as Json
	and extracts the data we want.
	"""
	def on_data(self,data):

		try:
			raw_data = json.loads(data)

			if 'text' in raw_data:

				username = raw_data['user']['screen_name']
				created_at = parser.parse(raw_data['created_at'])
				tweet = raw_data['text']
				retweet_count = raw_data['retweet_count']

				if raw_data['place'] is not None:
					place = raw_data['place']['country']
					print(place)
				else:
					place = None


				location = raw_data['user']['location']

				#insert data just collected into MySQL database
				connect(username, created_at, tweet, retweet_count, place, location)
				print("Tweet colleted at: {} ".format(str(created_at)))
		except Exception as e:
			print(e)


if __name__ == '__main__':

    # authentification so we can access twitter
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api =tweepy.API(auth, wait_on_rate_limit=True)

	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)
    # TODO: come up with tweet keywords
	track = ['#GOT','game of thrones','series finale']

	stream.filter(track=track, languages=['en'])
