from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import threading
import copy

#Variables that contains the user credentials to access Twitter API 
access_token = "157385150-JTgmvgmZwEcplQzUHSNpdEG1be98PYZWrJIJQ4st"
access_token_secret = "ERdu2dgOhicSqUbWlyyyi8xKWEcrT9vcxJ5W0HMVtbYmn"
consumer_key = "KPXnl72Vce8DCHFGec1UqbdVu"
consumer_secret = "wc6wq0wSeZmU4kTGPWXhvOqTMtsPOkjuRreNW8z2StK2JdJTVU"


class CustomListener(StreamListener):
    
    rollingStream = []
    twitterUsers = {}
    
    def on_data(self, data):
        x = json.loads(data)
        
        username = x['user']['screen_name']
        
        if self.twitterUsers.has_key(username):
            self.twitterUsers[username] += 1
        else:
            self.twitterUsers[username] = 1
        
        return True

    def on_error(self, status):
        print status

    def on_timer(self):
        threading.Timer(60.0, self.on_timer).start()
        print "\n****** report last 5 mins ******"
        
        #append it to the rolling list
        self.rollingStream.append(copy.deepcopy(self.twitterUsers))

        #reset the rolling list
        self.twitterUsers = {}

        #keep only last 5
        if len(self.rollingStream) > 5:
            del self.rollingStream[0]

        #print self.rollingStream
        #print stats
        combinedUserDict = {}
        for item in self.rollingStream:
            for key, val in item.iteritems():
                if not combinedUserDict.has_key(key):
                    combinedUserDict[key] = 0

                combinedUserDict[key] = combinedUserDict[key] + val 
        
        for key, val in combinedUserDict.iteritems():
            print key, ': ',  val


#This handles Twitter authetification and the connection to Twitter Streaming API
listener = CustomListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, listener) 

t=threading.Timer(60.0, listener.on_timer)
t.start()

#This line filter Twitter Streams to capture data by the keywords
stream.filter(track=['javascript'])
