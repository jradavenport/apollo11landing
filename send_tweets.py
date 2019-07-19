import tweepy
import pandas as pd
from datetime import datetime
from time import sleep
import numpy as np
import keys # DON'T PUT YOUR KEYS IN YOUR CODE!
auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.token, keys.token_secret)
api = tweepy.API(auth)


# Where this is running on my computer
dir = '/Users/james/Dropbox/Apps/apollo11landing/'

# read in the big table of Tweets, already prepped
df = pd.read_csv(dir + 'msgs.csv')

# took this idea from @bmorris3:
# https://github.com/bmorris3/transitingnow/blob/master/postEvents.py#L37
now = str(datetime.now())[:-10]

# find any tweets that should be sent now
to_post = df['time'].str[:-3] == now
if sum(to_post) > 0:
    tweets = df['msg'][to_post].values

    for twt in tweets:
        # send the actual tweet
        if twt[-1] == '.':
            twt = twt[0:-1]

        try:
            api.update_status(twt)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                # Do something special
                print('>>> duplicate message: ' + twt)

                twt = twt.replace('OK', np.random.choice(['OK', 'Okay', 'O.K.','ok', 'Ok']))
                twt = twt.replace('Roger', np.random.choice(['Roger', 'Roger..']))
                twt = twt.replace('...', np.random.choice(['...', '..', '. .']))
                twt = twt.replace('Copy', np.random.choice(['Copy', 'Copy..']))
                twt = twt.replace('Apollo11', np.random.choice(['Apollo11', 'Apollo 11']))
                twt = twt.replace('Stand by', np.random.choice(['Stand by', 'stand by..']))


                bks = np.random.choice(['; ', '| ', '- ', ';',':'])
                if len(twt) < 248:
                    xtra = np.random.choice([' #apollo50th', ' #apollo11', ' #apollo50', '  ', ' #nasa', ' #apollo', ' #moon'])

                api.update_status(twt.replace(': ',bks,1)+xtra)

        # be kind, take a pause
        if sum(to_post) > 1:
            sleep(50./sum(to_post))
