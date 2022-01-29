import tweepy
import pandas as pd
consumer_key="F2xoihNRNGPGqZWJlstb0kHuS"
consumer_secret="Cx32yanebJLE3Nqp0RkBG3YnJkeDqSE9QcqLS9LR2g5qyMmELp"
access_token="1276766738063872000-1J9Hpv03DHsxKcyqTMgJsUXefZLzpA"
access_token_secret="vS6sDgOLdUlWTTtKNmPQ4WcnPIvy57hvpIfcKGrR5dkIC"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweets_locs=[]

birthday = ['#happybd','#birthday','#happybirthday','#hbd','#bday']
child = ["#birth", "#childbirth", "#christening", "#childbearing", '#newparents', '#newborn']
marriage = ["#marriage", "#wedding", "#announcements", "#marriagegoals", "#hooked"]
vacation = ["#vacation", "#islandlife", "#travel", "#travelphotography", "#holidays", "#roadtrip", "#trip", "#adventure"]
graduation = ["#graduation", "#graduationday", "#graduate", "#graduating", '#convocation', '#graduated', '#graduationceremony'] 
career = ["#careergoals", "#newjob", "#gothired", "#firstdayfeeling", '#jobpromotion', '#firstdayjob', '#changingjob', '#newlyemployed']
relocation = ["#movingto", "#housing", "#relocate", "#relocation", '#newhome', '#newapartment', '#movinghouse', '#homeowner']
death = ['#saddemise', '#restinpeace', '#rip', '#passedaway', '#death']
divorce = ['#divorce', '#separated', '#divorced']
awards = ['#winningmoment', '#awarded', '#awardsandrewards', '#awardsandrecognition']
layoff = ['#furlough', '#layoff', '#dismissal']
education = ['#firstdayschool', '#kidscollege', '#kindergarten']
purchases = ['#newpurchase', '#newcar']
medical = ['#medicalemergency', '#hospitalized']
events = ['#publicevent', '#politicalevent', '#fundraising', '#charity']

for i in vacation:
  choice= i + "-filter:retweets"
  tweets = tweepy.Cursor(api.search_tweets,q=choice,lang="en",tweet_mode='extended').items(5000)
  for tweet in tweets:
    for media in tweet.entities.get("media",[{}]):
      if media.get("type",None) == "photo":
        continue
      elif media.get("type",None) == "video":
        continue
      else:
        tweets_locs.append([tweet.id,tweet.full_text,tweet.author,tweet.created_at,tweet.entities,tweet.geo,tweet.lang,tweet.in_reply_to_screen_name,tweet.in_reply_to_status_id,tweet.in_reply_to_user_id,tweet.retweet,tweet.retweet_count,tweet.retweets,tweet.retweeted,tweet.source,tweet.source_url,tweet.user,tweet.user.screen_name,tweet.user.url,tweet.user.translator_type,tweet.user.timeline,tweet.user.time_zone,tweet.user.name,tweet.user.lang,tweet.user.is_translator,tweet.user.is_translation_enabled,tweet.user.id,tweet.user.geo_enabled,tweet.user.entities, tweet.user.location]) 

tweet_text = pd.DataFrame(data=tweets_locs,columns=['id','text','author','created_at','entities','geo','lang','in_reply_to_screen_name','in_reply_to_status_id','in_reply_to_user_id','retweet','retweet_count','retweets','retweeted','source','source_url','user','user_screen_name','user_url','user_translator_type','user_timeline','user_time_zone','user_name','user_lang','user_is_translator','user_is_translation_enabled','user_id','user_geo_enabled','user_entities', 'user_location'])
tweet_text.to_csv("vacation.csv",index=False,sep=',')
print('Done')
