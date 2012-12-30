import requests
import json


DAILYMOTION_BASE_API_URL = 'https://api.dailymotion.com/'


def get(access_token, path, **query):
    if access_token:
        oauth_header = 'OAuth %s' % access_token
        headers = {'Authorization': oauth_header}
    else:
        headers = {}
    query_string = ''
    for key, value in query.iteritems():
        if value is not None:
            query_string += '%s=%s&' % (key, value)
    url = DAILYMOTION_BASE_API_URL + path + '?' + query_string[:-1]
    return json.loads(requests.get(url, headers=headers).content)


class Dailymotion(object):

    def __init__(self, access_token=None, path='', **query):
        self.access_token = access_token
        self.path = path
        self.query = query

    def users(self, page=None, limit=None):
        return PaginatedList(User, self.access_token, 'users', page=page, limit=limit)

    def user(self, username):
        return User(self.access_token, 'user/' + username)

    def me(self):
        return User(self.access_token, 'me/')

    def contests(self, page=None, limit=None):
        return PaginatedList(Contest, self.access_token, 'contests', page=page, limit=limit)

    def contest(self, id):
        return Contest(self.access_token, 'contest/' + id)

    def subtitle(self, id):
        return Subtitle(self.access_token, 'subtitle/' + id)

    def channels(self, page=None, limit=None):
        return PaginatedList(Channel, self.access_token, 'channels', page=page, limit=limit)

    def channel(self, id):
        return Channel(self.access_token, 'channel/' + id)

    def playlists(self, page=None, limit=None):
        return PaginatedList(Playlist, self.access_token, 'playlists', page=page, limit=limit)

    def playlist(self, id):
        return Playlist(self.access_token, 'playlist/' + id)

    def comment(self, id):
        return Comment(self.access_token, 'comment/' + id)

    def videos(self, page=None, limit=None, search=None):
        return PaginatedList(Video, self.access_token, 'videos', page=page, limit=limit, search=search)

    def video(self, id):
        return Comment(self.access_token, 'video/' + id)


class CachedMagicAttributes(Dailymotion):
    # this is a rather smart class so the name
    # doesn't cover everything yet

    def __init__(self, access_token=None, path='', values=None, **query):
        super(CachedMagicAttributes, self).__init__(access_token, path, **query)
        if values:
            self.cached = values
            for key, value in values.iteritems():
                setattr(self, key, value)
        else:
            self.cached = False

    def value(self):
        if not self.cached:
            self.cached = get(self.access_token, self.path, **self.query)
        return self.cached

    def __getattr__(self, attr):
        if not self.cached:
            self.value()
            for key, value in self.cached.iteritems():
                setattr(self, key, value)
            # return the value if it's found
            if attr in self.cached:
                return self.cached[attr]
        raise AttributeError


class PaginatedList(CachedMagicAttributes):

    def __init__(self, klass, access_token, path, **query):
        super(PaginatedList, self).__init__(access_token, path, **query)
        self.klass = klass

    def __call__(self):
        for element in self.list:
            yield self.klass(values=element)


def embed(url, maxwidth=None, maxheight=None, wmode=None, autoplay=False):
    service = 'http://www.dailymotion.com/services/oembed?format=json&url='
    url = service + url
    if wmode:
        url = url + '&wmode=' + wmode
    if maxheight:
        url = url + '&maxheight=' + maxheight
    if maxwidth:
        url = url + '&maxwidth=' + maxwidth
    if autoplay:
        url = url + '&autoplay=1'
    data = json.loads(requests.get(url).content)
    return Embed(values=data)


class Embed(CachedMagicAttributes):
    pass


class User(CachedMagicAttributes):

    def contests(self, page=None, limit=None):
        path = self.path + '/contests'
        return PaginatedList(Contest, self.access_token, path, page=page, limit=limit)

    def fans(self, page=None, limit=None):
        path = self.path + '/fans'
        return PaginatedList(User, self.access_token, path, page=page, limit=limit)

    def favorites(self, page=None, limit=None):
        path = self.path + '/favorites'
        return PaginatedList(Video, self.access_token, path, page=page, limit=limit)

    def features(self, page=None, limit=None):
        path = self.path + '/features'
        return PaginatedList(Video, self.access_token, path, page=page, limit=limit)

    def following(self, page=None, limit=None):
        path = self.path + '/following'
        return PaginatedList(User, self.access_token, path, page=page, limit=limit)

    def friends(self, page=None, limit=None):
        path = self.path + '/friends'
        return PaginatedList(User, self.access_token, path, page=page, limit=limit)

    def groups(self, page=None, limit=None):
        path = self.path + '/groups'
        return PaginatedList(Group, self.access_token, path, page=page, limit=limit)

    def playlists(self, page=None, limit=None):
        path = self.path + '/playlists'
        return PaginatedList(Playlist, self.access_token, path, page=page, limit=limit)

    def subscriptions(self, page=None, limit=None):
        path = self.path + '/subscriptions'
        return PaginatedList(Video, self.access_token, path, page=page, limit=limit)

    def videos(self, page=None, limit=None):
        path = self.path + '/videos'
        return PaginatedList(Video, self.access_token, path, page=page, limit=limit)


class Contest(CachedMagicAttributes):

    def members(self, page=None, limit=None):
        path = self.path + 'members/'
        return PaginatedList(User, self.access_token, path, page=page, limit=limit)

    def videos(self, page=None, limit=None):
        path = self.path + 'videos/'
        return PaginatedList(Video, self.access_token, path, page=page, limit=limit)


class Video(CachedMagicAttributes):

    class Subtitles(PaginatedList):

        def add(self):
            raise NotImplementedError

    class Comments(PaginatedList):

        def add(self):
            raise NotImplementedError

    class Groups(PaginatedList):

        def connected(self, id):
            raise NotImplementedError

        def connect(self, id):
            raise NotImplementedError

        def remove(self, id):
            raise NotImplementedError

    class Playlists(PaginatedList):
        pass

    def __init__(self, access_token=None, path='', values=None, **query):
        super(Video, self).__init__(access_token, path, values, **query)
        self.subtitles = self.Subtitles(Subtitle, access_token, path + 'subtitles/')
        self.comments = self.Comments(Comment, access_token, path + 'comments/')
        self.contests = PaginatedList(Contest, access_token, path + 'contests/')
        self.groups = self.Groups(Group, access_token, path + 'comments/')
        self.playlist = self.Playlists(Playlist, access_token, path + 'playlists/')
        self.related = PaginatedList(Video, access_token, path + 'related')


class Group(CachedMagicAttributes):

    class Members(PaginatedList):

        def connected(self, id):
            raise NotImplementedError

        def add(self):
            raise NotImplementedError

        def remove(self, id):
            raise NotImplementedError

    def __init__(self, access_token=None, path='', values=None, **query):
        super(Video, self).__init__(access_token=None, path='', values=None, **query)
        self.subtitles = self.Members(User, path + 'members/')


class Subtitle(CachedMagicAttributes):

    def post(self):
        raise NotImplementedError


class Channel(CachedMagicAttributes):

    def videos(self):
        return PaginatedList(Video, self.access_token, self.path + 'videos')


class Playlist(CachedMagicAttributes):

    class Videos(PaginatedList):

        def connected(self, id):
            raise NotImplementedError

        def post(self, *video_ids):
            raise NotImplementedError

        def remove(self, id):
            raise NotImplementedError

    def __init__(self, access_token=None, path='', values=None, **query):
        super(Video, self).__init__(access_token=None, path='', values=None, **query)
        self.videos = self.Videos(Video, path + 'videos/')


class Comment(CachedMagicAttributes):

    def post(self, **values):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
