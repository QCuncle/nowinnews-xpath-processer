import base64
import re
import time
from typing import Dict

from lxml import etree

from app.models import SiteNews, NewsItem


class ZhiHuXpathProcessor:
    def __init__(self):
        self.num_regex = re.compile(r'[^0-9]')
        self.url_regex = re.compile(r'"attached_info_bytes":"(.*?)"')

    def analyzing_articles(self, config: Dict, document: etree._Element, html: str) -> SiteNews:
        title_list = document.xpath(config['articleXpath']['title'])
        popularity_list = document.xpath(config['articleXpath'].get('popularity', ''))

        if config['articleXpath'].get('imageUrl', ''):
            img_url_list = document.xpath(config['articleXpath'].get('imageUrl', ''))
        else:
            img_url_list = []

        matches = self.url_regex.findall(html)
        url_list = [
            f"{config['host']}/{self._decode_article_id(base64_value)}?utm_division=hot_list_page"
            for base64_value in matches
        ]

        news_items = []
        for i in range(len(title_list)):
            item = NewsItem(
                siteCode=config['code'],
                siteName=config['name'],
                position=i + 1,
                title=title_list[i],
                url=url_list[i],
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

    def _decode_article_id(self, base64_value: str) -> str:
        base64_value = base64_value[52:66]
        decoded_bytes = base64.b64decode(base64_value)
        return self.num_regex.sub('', decoded_bytes.decode('utf-8'))

    def _format_url(self, host: str, url: str) -> str:
        if url.startswith("https://"):
            return url
        elif url.startswith("//"):
            return f"https:{url}"
        else:
            return f"{host}{url}"
