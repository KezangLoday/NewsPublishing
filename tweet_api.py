import tweepy
import configparser

import pandas as pd

#reading from configs for security
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authenthication of app to twitter api
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)



#using to get public tweets
api = tweepy.API(auth)

number_of_tweets = 5
store_tweets = []
author = []
time = []
image = []

for i in tweepy.Cursor(api.user_timeline, screen_name="thebhutanese", tweet_mode="extended", include_entities=True,).items(number_of_tweets):
   #store_tweets.append(i.full_text)
    author.append(i.author)
    time.append(i.created_at)
    image.append(i.entities['media']['media_url'])


df = pd.DataFrame({ 'time': time, 'author': image})


if __name__ == "__main__":
    print(df)
    # customerinfo = api.get_user('@thebhutanese')
    # print
    # "entities :", customerinfo.entities.get('description').get('urls')