import time
import requests

from redis import StrictRedis
from collections import namedtuple
from bs4 import BeautifulSoup
from common.cache import VisitedUrlCache, TargetUrlCache, QueuingUrlCache


Host = "http://www.zimuku.net/"
visited_cache = VisitedUrlCache()
target_cahche = TargetUrlCache()
queuing_cache = QueuingUrlCache()


class Spider(object):

    @staticmethod
    def join_url(host=Host, url=None):
        if url.startswith("/"):
            return Host + url[1:]
        return Host + url

    def _skip_url(self, url):
        if url.startswith("http"):
            return True
        return False

    def _target_url(self, url):
        return url.startswith("/detail")

    def parse(self, response):
        """get all urls in this website but cannot include other sites url"""
        urls = []
        try:
            soup = BeautifulSoup(response, "html.parser")
        except Exception as e:
            return False, urls

        for link in soup.find_all('a'):
            if 'class' in link:
                continue
            url = link.get("href", None)
            if not url:
                continue

            # judge if need to skip this url by some page tokenlize
            if self._skip_url(url):
                print("{} isn.t needed url".format(url))
                continue

            # url is target url
            if self._target_url(url):
                print("{} is target url".format(url))
                target_cahche.add_urls(self.join_url(url=url))
                continue

            # no target url maybe has target urls' url
            urls.append(self.join_url(url=url))

        return True, urls

    def crawl(self, url):
        try:
            r = requests.get(url)
        except Exception as e:
            print("crawl [{}] failed".format(url))
            return False, None
        ok, urls = self.parse(r.content)
        print("crawl [{}] done".format(url))
        return ok, urls


class Controller(object):
    ori_page = 1
    ori_host_fmt = "http://www.zimuku.net/newsubs?ad=1&p={page}"
    is_first_spider = True
    max_page = 50

    def __init__(self):
        self.spider = Spider()

        # if first run spider process
        if self.check_is_first_spider():
            _urls = []
            for i in range(self.max_page):
                _url = self.ori_host_fmt.format(page=i + 1)
                _urls.append(_url)

            queuing_cache.add_urls(_urls)
            now_queuing_cnt = queuing_cache.scount()
            print("Puting init urls into QueuingUrlCache done, now queuing urls count is {}".format(
                now_queuing_cnt))

        print("Controller init done")

    def check_is_first_spider(self):
        """检查是不是第一次启动爬虫，或者启动的第一个爬虫程序"""
        return queuing_cache.is_existed()

    def filter_urls(self, urls):
        print("before filter count: {}".format(len(urls)))
        urls = filter(lambda url: not visited_cache.is_in(url), urls)
        urls = filter(lambda url: not queuing_cache.is_in(url), urls)
        urls = list(urls)
        print("after filter count: {}".format(len(urls)))
        return urls

    def append_url_into_cache(self, urls):
        urls = self.filter_urls(urls)
        len_of_urls = len(urls)
        if len_of_urls <= 10:
            queuing_cache.add_urls(tmp_urls)
            return len_of_urls

        # !!!! 这里好像有问题
        cnt = 0
        tmp_urls = []
        for url in urls:
            cnt += 1
            tmp_urls.append(url)
            if cnt <= 10:
                continue
            queuing_cache.add_urls(tmp_urls)
            # reset counter and urls container
            cnt = 0
            tmp_urls = []

        return len_of_urls

    def run(self):
        print("Spider running....")
        while True:
            time.sleep(0.5)
            url = queuing_cache.get_one_url()
            if not url:
                print("No url in queuing, Spider sleep 3 seconds")
                time.sleep(3)
                continue

            # crawl running
            ok, urls = self.spider.crawl(url)

            # crawl failed, send this failed url back into queuing urls
            if not ok:
                print(
                    "Put url back into QueuingUrlCache: {}, reason=['Crawl failed']".format(url))
                queuing_cache.add_urls(url)
                continue

            # crawl ok, append urls into VisitedUrlCache
            visited_cache.add_urls(url)
            cnt = self.append_url_into_cache(urls)
            print("update queuing urls count: {}".format(cnt))


if __name__ == "__main__":
    c = Controller()
    c.run()
