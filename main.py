"""

TW Interaction Puller
by @tonsai
License : MIT License

"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from config import config, pushbullet_token
from pushbullet import PushBullet
import json

p = PushBullet(pushbullet_token)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        data = json.loads(data)
        if "text" in data and "@tonsai" in data["text"]:
            print data["user"]["screen_name"], ":", data["text"].encode("utf-8")
            msg_title = "Mention from @" + str(data["user"]["screen_name"])
            msg_body = data["text"].encode("utf-8")
            p.push_note(msg_title, msg_body)
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])

    stream = Stream(auth, l)
    stream.userstream()