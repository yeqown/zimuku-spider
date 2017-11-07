import requests
import time
import sys
import json
import os.path as path

from bs4 import BeautifulSoup

common_path = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(common_path)

from common.cache import DownedUrlCache, WaitDownloadUrlCache


waitdownload_cache = WaitDownloadUrlCache()
downed_cache = DownedUrlCache()
headers = {
    'cache-control': "no-cache",
    'postman-token': "c874d4d5-cc54-c627-1bb1-778ea32b868b"
}

download_filepath = lambda file: path.abspath(
    path.join(path.dirname(__file__), "../data/download_corpus/{}".format(file)))
loads_url = lambda dumped_url: json.loads(dumped_url)


class Downloader(object):

    def __init__(self):
        self.s = requests.Session()
        # self.s.headers = headers
        # self.s.get("http://www.zimuku.net")
        # self.s.max_redirects = 50

    def download(self, url, name):
        print("[{}] Downloading".format(name))
        r = self.s.get(url, headers=headers)
        try:
            with open(download_filepath(name), "wb") as f:
                f.write(r.content)
        except Exception as _:
            print("[{}] Download failed".format(name))
            return False
        print("[{}] Download success".format(name))
        return True

    def run(self):
        while True:
            time.sleep(0.5)
            dumped_url = waitdownload_cache.get_one_url()
            # print("\n", dumped_url, "\n")

            if not dumped_url:
                print("Didn-t get wait-download-url, so sleep 3 secs")
                time.sleep(3)
                continue
            try:
                url_obj = loads_url(dumped_url)
            except Exception as _:
                continue
            url = url_obj.get("url")
            name = url_obj.get("name")
            ok = self.download(url, name)
            if ok:
                downed_cache.add_urls(url)
                continue
            # waitdownload_cache.add_urls(dumped_url)

if __name__ == "__main__":
    d = Downloader()
    d.run()
