import re
import sys
import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plot

search_term = ""
tweets_count = 0
def cleanTweet(tweet):
 return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweets():
 global search_term, tweets_count
 auth = tweepy.OAuthHandler("<consumer_key>", "<consumer_secret>") #Your API Consumer Keys
 auth.set_access_token("<access_token>", "<access_token_secret>") #Your API Access tokens
 api = tweepy.API(auth)
 
 search_term = raw_input("Search Keyword for requesting tweets : ") #Search Keyword
 tweets_count = int(raw_input("Number of tweets to request : ")) #Number Tweets

 tweets = tweepy.Cursor(api.search, q=search_term).items(tweets_count)
 non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

 print "Requesting tweets for keyword '"+search_term+"'...."
 tweet_list = [cleanTweet(tweet=tweet.text.translate(non_bmp_map)).encode("utf8") for tweet in tweets]
 return pd.DataFrame({"Tweets":tweet_list})

def analyse_tweets():
 global search_term, tweets_count
 tweets_df = get_tweets()
 if len(tweets_df["Tweets"]) == 0:
  print "0(Zero) Tweets found for search key word '"+search_term+"'"
  return
 print "Analysing tweets..."
 tweets_df["Polarity"] = [TextBlob(text.decode('utf-8').strip()).sentiment.polarity for text in tweets_df["Tweets"]] #Calculating sentiment polarity
 tweets_df["Subjectivity"] = [TextBlob(text.decode('utf-8').strip()).sentiment.subjectivity for text in tweets_df["Tweets"]] #Calculating sentiment subjectivity

 y= [0, 0, 0]

 for polarity in tweets_df["Polarity"]:
  if polarity > 0:
   y[0] = y[0]+1
  elif polarity < 0:
   y[2] = y[1]+1
  else:
   y[1] = y[2]+1
 x = ["Positive", "Neutral", "Negative"]
 y = [float(value*100/tweets_count) for value in y]
 explode = (0.1, 0.05, 0.025)
 plot.pie(y, explode=explode, labels=x, autopct='%1.1f%%', shadow=True, startangle=140)
 plot.title("How people are reactive on '"+search_term+"'");

 print "Storing Analysed tweets to tweet_analysis_of_"+search_term+".csv"
 tweets_df.to_csv("./tweet_analysis_of_"+search_term.replace(" ", "_")+".csv", index=False);
 print "Saving Plot to tweet_analysis_of_"+search_term+".png"
 plot.savefig("./tweet_analysis_of_"+search_term.replace(" ", "_")+".png")
 plot.show()

analyse_tweets()