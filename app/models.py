from dataclasses import dataclass
from typing import List


@dataclass
class NewsItem:
    siteCode: str
    siteName: str
    position: int
    title: str
    url: str
    imageUrl: str
    popularity: str


@dataclass
class SiteNews:
    siteCode: str
    siteName: str
    siteIconUrl: str
    updateTimestamp: int
    data: List[NewsItem]
