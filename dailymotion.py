import requests
import json


class MagicDict(object):

    def __init__(self, d):
        for key, value in d.iteritems():
            setattr(self, key, value)


class Embed(MagicDict):
    pass


class User(MagicDict):
    pass


def embed(url):
    # FIXME: add maxwidth, maxheight, wmode
    # http://www.dailymotion.com/doc/api/oembed.html#oembed
    service = 'http://www.dailymotion.com/services/oembed?format=json&url='
    url = service + url
    data = json.loads(requests.get(url).content)
    return MagicDict(data)


class Dailymotion(object):

    service = 'https://api.dailymotion.com/'
    base_path = ''

    def __init__(self, access_token=None):
        self.access_token = access_token

    def __get(self, path, query):
        oauth_header = 'OAuth %s' % self.access_token
        headers = {'Authorization': oauth_header}
        query_string = ''
        for key, value in query.iteritems():
            query_string += '%s=%s&' % (key, value)
        path = self.base_path + path
        url = self.service + path + '?' + query_string
        return requests.get(url, headers=headers)

    def user(self, username):
        path = 'user/%s/' % username
        return DailymotionUser(path, self.access_token)

    def me(self):
        return DailymotionUser('me/', self.access_token)


class DailymotionUser(Dailymotion):

    def __init__(self, user_path, access_token):
        self.base_path = user_path
        self.access_token = access_token

    def data(self):
        r = self.__get()
        return User(r)
