# -*- coding: utf-8 -*-
import sys
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

def get_twitter_auth():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
     
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

class CustomListener(StreamListener):
    """Custom StreamListener for streaming Twitter data."""

    def __init__(self, fname):
        safe_fname = format_filename(fname)
        # self.outfile = "stream_%s.jsonl" % safe_fname
        # self.outfile = "stream_{}_{}.jsonl".format(safe_fname, time.strftime('%Y-%m-%d-%H',time.localtime(time.time())))
        # self.outfile = "stream_{}.jsonl".format(time.strftime('%Y-%m-%d-%H',time.localtime(time.time())))

    def on_data(self, data):
        try:
            print ("In Writing")
            # with open("twitter_{}_{}.jsonl".format(time.strftime(str(StreamListener), '%Y-%m-%d-%H-%M',time.localtime(time.time()))), 'a') as f:
            # with open(self.outfile, 'a') as f:
            with open("/home/ubuntu/work/stream_{}.jsonl".format(time.strftime('%Y-%m-%d-%H',time.localtime(time.time()))), 'a') as f:
                f.write(data)
            print (time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time())))
            return True
        except BaseException as e:
            print ("BaseException")
            sys.stderr.write("Error on_data: {}, sleep 5s\n".format(e))
            time.sleep(5)
            return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True

def format_filename(fname):
    """Convert fname into a safe string for a file name.

    Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if "invalid".

    Return: string
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

if __name__ == '__main__':
    print ("query = sys.argv[1:]")
    query = sys.argv[1:] # list of CLI arguments
    print ("query_fname = ' '.join(query)")
    query_fname = ' '.join(query) # string
    print ("auth = get_twitter_auth()")
    auth = get_twitter_auth()
    print ("twitter_stream = Stream(auth, CustomListener(query_fname))")
    twitter_stream = Stream(auth, CustomListener(query_fname))
    print ("twitter_stream.filter(track=query, async=True)")
    twitter_stream.filter(track=query, async=True)
