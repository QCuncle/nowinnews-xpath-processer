import time
from typing import Dict

from lxml import etree

from app.models import SiteNews, NewsItem


class PositionXpathProcessor:
    def analyzing_articles(self, config: Dict, document: etree._Element) -> SiteNews:
        positions = document.xpath(config['articleXpath']['position'])
        title_list = document.xpath(config['articleXpath']['title'])
        popularity_list = document.xpath(config['articleXpath'].get('popularity', ''))
        url_list = document.xpath(config['articleXpath']['url'])

        if config['articleXpath'].get('imageUrl', ''):
            img_url_list = document.xpath(config['articleXpath'].get('imageUrl', ''))
        else:
            img_url_list = []

        news_items = []
        real_position = 0
        for jx_node in positions:
            try:
                p_value = int(jx_node)

                # Safe to call subsequent code if p_value is a valid integer
                item = NewsItem(
                    siteCode=config['code'],
                    siteName=config['name'],
                    position=p_value,
                    title=title_list[real_position + 1],
                    url=self._format_url(config['host'], url_list[real_position + 1]),
                    imageUrl=self._format_url(config['host'],
                                              img_url_list[real_position + 1]) if img_url_list else "",
                    popularity=popularity_list[real_position] if popularity_list else "",
                )
                news_items.append(item)
                real_position = real_position + 1
            except ValueError:
                print(f'Invalid integer value: {jx_node}')
                continue

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
