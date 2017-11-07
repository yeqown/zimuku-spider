from redis import StrictRedis, ConnectionPool

_pool = ConnectionPool(host="127.0.0.1", port=6379, db=0)


class Cache(StrictRedis):

    def __init__(self):
        super().__init__(connection_pool=_pool)

    def key(self):
        raise NotImplementedError

    def scount(self):
        return self.scard(self.key())

    def is_existed(self):
        return self.exists(self.key())


class UrlCache(Cache):

    def is_in(self, url):
        return self.sismember(self.key(), url)

    def add_urls(self, url_or_urls):
        if isinstance(url_or_urls, (list)):
            self.sadd(self.key(), *url_or_urls)
        else:
            self.sadd(self.key(), url_or_urls)

    def get_one_url(self):
        return self.spop(self.key())


class DownedUrlCache(UrlCache):

    def key(self):
        return "url:downed"


class VisitedUrlCache(UrlCache):

    def key(self):
        return "url:visited"


class QueuingUrlCache(UrlCache):

    def key(self):
        return "url:queuing"


class TargetUrlCache(UrlCache):

    def key(self):
        return "url:target"


class WaitDownloadUrlCache(UrlCache):

    def key(self):
        return "url:waitdownload"


class HasParsedTargetCache(UrlCache):

    def key(self):
        return "url:target:hasparsed"
