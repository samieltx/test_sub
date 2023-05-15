
import logging
import feedparser
from gnews import GNews
import pandas as pd

from tienda_amiga.cfg import (
    BASE_URL,
    DATA_DIR,
    USER_AGENT,
)

class GNews_wo_import(GNews):
    def get_full_article(self, url: str):
        try:
            from newspaper import Article

            article = Article(url="%s" % url, language=self._language)
            article.download()
            article.parse()
        except Exception as error:
            logger = logging.getLogger(__name__)
            logger.error(error.args[0])
            return None
        return article

    def get_news(self, key):
        """
        :return: JSON response as nested Python dictionary.
        """
        if key:
            key = "%20".join(key.split(" "))
            url = BASE_URL + '/search?q={}'.format(key) + self._ceid()
            return self._get_news(url)

    def _get_news(self, url):
        try:
            if self._proxy:
                proxy_handler = urllib.request.ProxyHandler(self._proxy)
                feed_data = feedparser.parse(
                    url, agent=USER_AGENT, handlers=[proxy_handler]
                )
            else:
                feed_data = feedparser.parse(url, agent=USER_AGENT)

            return [
                item
                for item in map(self._process, feed_data.entries[: self._max_results])
                if item
            ]
        except Exception as err:
            logging.info(err.args[0])
            return []


def get_news_from_api(topic, max_results=10):
    logging.info(f"Getting news from the GNews API... \n")

    key = topic
    key = "%20".join(key.split(" "))
    url = BASE_URL + '/search?q={}'.format(key)
    feed_data = feedparser.parse(url, agent=USER_AGENT)
    google_news = GNews_wo_import(max_results=max_results)
    rv = [
        item
        for item in map(
            google_news._process, feed_data.entries[: google_news._max_results]
        )
        if item
    ]
    articles = [google_news.get_full_article(r['url']) for r in rv]
    articles = [article for article in articles if article is not None]
    df = pd.DataFrame([x.__dict__ for x in articles])
    df.to_csv(DATA_DIR / "data_bitcoin.csv", index=False)
    
