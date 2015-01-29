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

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_status(self, status):
        """ Filter if this tweet mentioned you, then push it to PushBullet """
        if config["username"] in status.text:
            data = { "sender":status.author.screen_name.encode("utf-8"),
                     "text":status.text.encode("utf-8")
                   }
            print "R | @" + data["sender"] + ": " + data["text"]
            self.push(data)
            return True

    def on_direct_message(self, data):
        """ Filter if this DM belong to you, then push it to PushBullet """
        if config["username"][1:] in data.direct_message["recipient_screen_name"]:
            data = { "sender": data.direct_message["sender_screen_name"].encode("utf-8"),
                     "recipient": data.direct_message["recipient_screen_name"].encode("utf-8"),
                     "text": data.direct_message['text'].encode("utf-8")
                   }
            print "D | @" + data["sender"] + ": " + data["text"]
            self.push(data)
            return True

    def on_disconnect(self, notice):
        text = notice.code, ":", notice.reason
        print "DISCONNECTED! (" + text + ")"
        p.push_note('Puller disconnected!', text)
        exit()
        return True

    def on_warning(self, notice):
        text = notice.code, ":", notice.message, "(" + notice.percent_full + "%)"
        print "STALL WARNING! (" + text + ")"
        p.push_note('STALL WARNING!', text)
        return True

    def push(self, data):
        """ Push the given data to PushBullet """
        if "recipient" in data:
            msg_title = "New DM from @" + data["sender"]
        elif data["text"][:3] == "RT " and config["username"] in data["text"]:
            msg_title = "@" + data["sender"] + " retweeted your tweet."
        else:
            msg_title = "New mention from @" + data["sender"]
        msg_body = data["text"]
        p.push_note(msg_title, msg_body)
        return True

if __name__ == '__main__':
    l = StdOutListener()
    p = PushBullet(pushbullet_token)
    auth = OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])

    stream = Stream(auth, l)
    stream.userstream(_with="user", stall_warnings=True)
