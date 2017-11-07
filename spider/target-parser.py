import requests
import time
import sys
import json
import os.path as path

from bs4 import BeautifulSoup

common_path = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(common_path)

from common.cache import TargetUrlCache, WaitDownloadUrlCache, HasParsedTargetCache

waitdownload_cache = WaitDownloadUrlCache()
target_cache = TargetUrlCache()
parsed_cache = HasParsedTargetCache()

dumps_url = lambda name, url: json.dumps({"name": name, "url": url})


class TargetUrlParser(object):

    def join_download_url(self, url):
        return "http://www.zimuku.net" + url

    def parse(self, content):
        soup = BeautifulSoup(content, "html.parser")
        a_tag = soup.find('a', id="down1")
        if not a_tag:
            print("didn-t find item [a] with id-`down1`")
            return False

        div_tag = soup.find("div", attrs={"class": "md_tt prel"})
        h1_tag = div_tag.h1

        if not h1_tag:
            print("didn-t match item [h1] with xpath")
            return False

        download_url = a_tag.get("href", None)
        if not download_url:
            print("didn-t match download url")
            return False

        name = h1_tag.get("title", None)
        if not name:
            print("didn-t match [h1] has title attribute")
            return False

        download_url = self.join_download_url(download_url)
        dumped_url = dumps_url(name, download_url)
        waitdownload_cache.add_urls(dumped_url)
        print("append {} into WaitDownloadUrlCache".format(download_url))
        return True

    def run(self):
        while True:
            time.sleep(1)
            url = target_cache.get_one_url()
            if not url:
                print("Downloader did not get any target url, so sleep for 3 secs")
                time.sleep(3)
            # parsed target url, skip this
            if parsed_cache.is_in(url):
                print("Skip this {} - url in HasParsedTargetCache".format(url))
                continue
            r = requests.get(url)
            ok = self.parse(r.content)
            # parse ok, so add url into parsed cache
            if ok:
                print("HasParsedTargetCache append {}".format(url))
                parsed_cache.add_urls(url)
                continue
            # didn't download success so put this url back
            target_cache.add_urls(url_or_urls=url)


if __name__ == "__main__":
    tp = TargetUrlParser()
    tp.run()
