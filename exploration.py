import psycopg2
import os
import re
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import matplotlib.pyplot as plt


class TweetObject(object):
    def __init__(self, host, database, user):
        self.password = os.environ["password"]
        self.host = host
        self.database = database
        self.user = user


    def postgres_connect(self, query):
        """
		Connects to database and extracts
		raw tweets and any other columns we
		need
		Parameters:
		----------------
		arg1: string: SQL query
		Returns: Pandas Dataframe
		----------------
		"""

        try:
            conn = psycopg2.connect(host=self.host, database=self.database, \
                                    user=self.user, password=self.password)
            print('Successfully connected to database')
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['created_at','tweet'])

        except Exception as e:
            print(e)

        cursor.close()
        conn.close()
        return df

    def clean_tweets(self, df):
        # Do some text preprocessing
        stopword_list = stopwords.words('english')
        ps = PorterStemmer()
        df["clean_tweets"] = None
        df['len'] = None
        try:
            for i in range(0,len(df['tweet'])):
                # get rid of anythin that isnt a letter
                exclusion_list = ['[^a-zA-Z]','rt', 'http', 'co', 'RT']
                exclusions = '|'.join(exclusion_list)
                text = re.sub(exclusions, ' ' , df['tweet'][i])
                text = text.lower()
                words = text.split()
                words = [word for word in words if not word in stopword_list]
                # only use stem of word
                words = [ps.stem(word) for word in words]
                df['clean_tweets'][i] = ' '.join(words)
                print('Tweet cleaned!')
            df['len'] = np.array([len(tweet) for tweet in df["clean_tweets"]])
            print('Done Cleaning!!')
        except TypeError:
            print(df.head())
        return df

    def sentiment(self, tweet):
        """
		This function calculates sentiment
		on our cleaned tweets.
		Uses textblob to calculate polarity.
		Parameters:
		----------------
		arg1: takes in a tweet (row of dataframe)
		"""

        analysis = TextBlob(tweet)

        if analysis.sentiment.polarity > 0:
            print('Assigned tweet Sentiment Analysis of positive!')
            return 1
        elif analysis.sentiment.polarity == 0:
            print('Assigned tweet Sentiment Analysis of neutral!')
            return 0
        else:
            print('Assigned tweet Sentiment Analysis of negative!')
            return -1


    def save_to_csv(self, df):
        """
		Save cleaned data to a csv for further
		analysis.
		Parameters:
		----------------
		arg1: Pandas dataframe
		"""

        try:
            df.to_csv("data/clean_tweets.csv")
            print("\n")
            print("csv successfully saved. \n")

        except Error as e:
            print(e)

    def word_cloud(self, df):
        plt.subplots(figsize = (12,10))
        wordcloud = WordCloud(
                background_color = 'white',
                width = 1000,
                height = 800).generate(" ".join(df['clean_tweets']))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':

    t = TweetObject(host='localhost', database='tweetsdb', user='troy')
    data = t.postgres_connect("SELECT created_at, tweet FROM tweets;")
    data = t.clean_tweets(data)
    data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])
    #t.word_cloud(data)
    t.save_to_csv(data)

    pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
    neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]

	#Print results
    print("percentage of positive tweets: {}%".format(100*(len(pos_tweets)/len(data['clean_tweets']))))
    print("percentage of negative tweets: {}%".format(100*(len(neg_tweets)/len(data['clean_tweets']))))
    print("percentage of neutral tweets: {}%".format(100*(len(neu_tweets)/len(data['clean_tweets']))))
