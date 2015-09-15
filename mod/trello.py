import requests
from requests_oauthlib import OAuth1
import selenium
from os.path import isfile


class TrelloBoard(object):
    def __init__(self, key=None, secret_key=None, v=False):
        self.key = key
        self.secret_key = secret_key

        if isfile('token.cache'):
            if v:
                print "Attempting to read previously created token..."

            with open('token.cache', 'r') as f:
                self.token = f.read()

        else:
            if v:
                print "Generating a new token..."

            self.token = self.generate_token()

    def generate_url(self):
        return "https://api.trello.com/1/boards/" + self.key

    def generate_token(self):
        auth = OAuth1(self.key, self.secret_key)
        u = 'https://trello.com/1/OAuthGetRequestToken'
        r = requests.get(u, auth=auth)

        b = r.text
        print b

        'https://trello.com/1/OAuthAuthorizeToken'

        with open('token.cache', 'w') as f:
            f.write(b)

        r.close()
        return b

    def get_member_record(self):
        u = "https://trello.com/1/members/me?key=%s&token=%s" % (
            self.key, self.token)

        print u

        return self.obtain_json_obj(u)

    def get_open_boards(self):
        u = "https://trello.com/1/members/my/boards?key=%s&token=%s" % (
            self.key, self.token)
        return self.obtain_json_obj(u)

    def get_pinned_boards(self):
        u = "https://trello.com/1/members/my/boards/pinned?key=%s&token=%s" % (
            self.key, self.token)
        return self.obtain_json_obj(u)

    def obtain_json_obj(self, url):
        r = requests.get(url, stream=True)
        obj = r.raw.read()
        r.close()
        return obj
