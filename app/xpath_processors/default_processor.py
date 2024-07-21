import time
from typing import Dict

from lxml import etree

from app.models import SiteNews, NewsItem


class DefaultXpathProcessor:
    def analyzing_articles(self, config: Dict, document: etree._Element) -> SiteNews:
        title_list = document.xpath(config['articleXpath']['title'])
        popularity_list = document.xpath(config['articleXpath'].get('popularity', ''))
        if config['articleXpath'].get('imageUrl', ''):
            img_url_list = document.xpath(config['articleXpath'].get('imageUrl', ''))
        else:
            img_url_list = []
        url_list = document.xpath(config['articleXpath']['url'])

        min_size = min(
            len(title_list),
            len(url_list),
            len(popularity_list) if popularity_list else len(title_list),
            len(img_url_list) if img_url_list else len(title_list)
        )

        news_items = []
        for i in range(min_size):
            item = NewsItem(
                siteCode=config['code'],
                siteName=config['name'],
                position=i + 1,
                title=title_list[i],
                url=self._format_url(config['host'], url_list[i]),
                imageUrl=self._format_url(config['host'], img_url_list[i]) if img_url_list else "",
                popularity=popularity_list[i] if popularity_list else "",
            )
            news_items.append(item)

        site_news = SiteNews(
            siteCode=config['code'],
            siteName=config['name'],
            siteIconUrl=config['siteIconUrl'],
            updateTimestamp=int(time.time() * 1000),
            data=news_items
        )
        return site_news

    def _format_url(self, host: str, url: str) -> str:
        if url.startswith("https://"):
            return url
        elif url.startswith("//"):
            return f"https:{url}"
        else:
            return f"{host}{url}"
