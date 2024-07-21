import time
from typing import Dict

from lxml import etree

from app.models import SiteNews, NewsItem


class TitleXpathProcessor:
    def analyzing_articles(self, config: Dict, document: etree._Element) -> SiteNews:
        title_list = document.xpath(config['articleXpath']['title'])
        popularity_list = document.xpath(config['articleXpath'].get('popularity', ''))
        if config['articleXpath'].get('imageUrl', ''):
            img_url_list = document.xpath(config['articleXpath'].get('imageUrl', ''))
        else:
            img_url_list = []
        url_list = document.xpath(config['articleXpath']['url'])

        news_items = []
        popularity_index = 0
        for i in range(1, len(title_list)):
            item = NewsItem(
                siteCode=config['code'],
                siteName=config['name'],
                position=i,
                title=title_list[i],
                url=self._format_url(config['host'], url_list[i]),
                imageUrl=self._format_url(config['host'], img_url_list[i]) if img_url_list else "",
                popularity=popularity_list[popularity_index] if popularity_list else "",
            )
            news_items.append(item)
            popularity_index += 1

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
