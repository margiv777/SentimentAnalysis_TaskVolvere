#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tweepy
from textblob import TextBlob
consumer_key = 'IEatkTI9Y8bQM6u91JmpsBDFK' #APIKey
consumer_secret = 'Uu84d9v1CqSx6VuFi48GuIJAm5jrivYR0xIPa1WqjPTMWPzFqN' #APIKeySecret
access_token = '1207004418530398208-Wp7BBNUajY6TR9sME7W0nfFP0X7xAv'
access_token_secret = 'e9lE8M3mmoA9hnJtmMYzchftGqNq8mXT29kbSJPkfWB9W'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token.access_token_secret)
api = tweepy.API(auth)
public_tweets = api.search('Elon Musk')
for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)


# In[7]:


import facebook as fb
import requests
import argparse
import textblob as tb

FLAGS = None

def sentiment_analysis(post):

    # Here's where the magic happens
    tb_msg = tb(post['message'])
    score = tb_msg.sentiment

    print("Date: %s, From: %s\n", post['created_time'], post['from'])
    print("%s\nShared: %s, Score: %f", post['message'], post['share'], score)



def connect(access_token, user):
    graph = fb.GraphAPI(access_token)
    profile = graph.get_object(user)

    return graph, profile


def main():

    access_token = FLAGS.access_token
    user = FLAGS.profile

    graph, profile = connect(access_token, user)
    
    posts = graph.get_connections(profile['id'], 'posts')


    #Let's grab all the posts and analyze them!
    while True:
        try:
            [sentiment_analysis(post=post) for post in posts['data']]
            posts= requests.get(posts['paging']['next']).json()
        except KeyError:
            break
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Facebook Sentiment Analysis Script')
    parser.add_argument('--access_token', type=str, required=True, default='', help='Your Facebook API Access Token: https://developers.facebook.com/docs/graph-api/overview')
    parser.add_argument('--profile', type=str, required=True, default='', help='The profile name to retrieve the posts from')
    FLAGS = parser.parse_args()
    main()


# In[ ]:




