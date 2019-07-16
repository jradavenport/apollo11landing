import tweepy
import pandas as pd
from datetime import datetime
from time import sleep
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

        xtra = ''
        if len(twt) < 248:
            xtra = ' #apollo50th'
        elif len(twt) > 248 & len(twt) < 250:
            xtra = ' #apollo50'
        # api.update_status(twt+xtra)
        try:
            api.update_status(twt)

        except tweepy.TweepError as error:
            if error.api_code == 187:
                # Do something special
                print('>>> duplicate message: ' + twt)
                api.update_status(twt.replace(':',';',1)+xtra)
            # else:
            #    raise error

        # be kind, take a pause
        sleep(50./sum(to_post))

    # update the silly "sent" column
    # df.at[to_post, 'sent'] = 1
    # write it back out!
    # df.to_csv(dir + 'msgs.csv')
