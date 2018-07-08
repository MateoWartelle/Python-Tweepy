#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import urllib

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
''' HELPER FUNCTIONS '''
def download_video_from_url(url, nameofvideo):
    urllib.request.urlretrieve(url, nameofvideo)
    return

''' GETTERS '''
def get_all_tweets_to_JSON(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))
       
    #write tweet objects to JSON
    file = open('tweet.json', 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
    
    #close the file
    print ("Done")
    file.close()

def get_JSON_from_tweet_id(tweet_id):    
    #write tweet objects to JSON
    file = open('one_tweet.json', 'w')
    try:
        tweet = api.get_status(id=tweet_id)
        json.dump(tweet._json,file,sort_keys = True, indent = 4)
        #close the file
        print ("Done")
        file.close()
    except tweepy.error.TweepError:
        print ("Unable to get status of tweet")
        file.close()

def get_video_from_tweet(tweet_id, jsonfile, nameofvideo):
    #write tweet objects to JSON
    originalnameofvideo = nameofvideo
    file = open(jsonfile, 'w') 
    tweet = api.get_status(id=tweet_id)
    json_out = json.dump(tweet._json,file,sort_keys = True, indent = 4)
    file.close()
    #read in JSON parse for the video links and download all three of them
    config = json.loads(open(jsonfile).read())
    duration = config['extended_entities']['media'][0]['video_info']['duration_millis']
    print("Duration is " + str(duration) + " millis")
    aspect = config['extended_entities']['media'][0]['video_info']['aspect_ratio']

    print("Aspect ratio is " + ''.join(str(aspect)))
    first_video_url = config['extended_entities']['media'][0]['video_info']['variants'][0]['url']
    nameofvideo = nameofvideo + ".mp4"
    print(originalnameofvideo + ".mp4" + " bitrate is 256000")
    download_video_from_url(first_video_url, nameofvideo)
    nameofvideo = originalnameofvideo + "_second.mp4"
    print(originalnameofvideo + "_second.mp4" + " bitrate is 832000")
    second_video_url = config['extended_entities']['media'][0]['video_info']['variants'][1]['url']
    download_video_from_url(second_video_url, nameofvideo)
    
    #close the file
    print ("Done")
    file.close()
  
''' TWEETING '''
def tweet_number_of_photos_from_folder(dirpath, numberofphotos):
    counter = 0
    for imagePath in os.listdir('.'):
        if os.path.isfile(imagePath):
            if not imagePath.startswith('.'):
                api.update_with_media(imagePath)
                counter = counter + 1
            if counter == numberofphotos:
                break
    print("Done")
    return

''' RETWEETING '''   
def retweet_all_from_specific_user(userid):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    results = api.statuses.user_timeline(screen_name=userid)
    for status in results:
        print("@%s %s %s" % (userid, status["text"], status['id']))
        try:
            # don't retweet your own tweets
            if status["user"]["screen_name"] == TWITTER_HANDLE:
                continue
            i = 60 + random.randint(1, 10) * random.randint(1, 10)
            print("wait {} seconds...".format(i))
            time.sleep(i)
            result = t.statuses.retweet(id=status["id"])
            print("retweeted: %s" % (result["text"].encode("utf-8")))
            result_fav = t.favorites.create(_id=status["id"])
            print("favorited: %s" % (result_fav["text"].encode("utf-8")))

        # when you have already retweeted a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))
    
if __name__ == '__main__':
    # pass in the tweetid you want to download to JSON file
    get_JSON_from_tweet_id("1015688256170680320")
    # pass in the username of the account you want to download to JSON file
    get_all_tweets_to_JSON("@FilmEasterEggs")
    # pass in the tweetid, json name for new file, name of video file (NO Extension)
    get_video_from_tweet("1015265582965407744", "video_file.json", "test")    
