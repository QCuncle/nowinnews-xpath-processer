from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional

from lxml import etree
from playwright.async_api import async_playwright

from app.models import SiteNews
from app.xpath_processors.default_processor import DefaultXpathProcessor
from app.xpath_processors.position_processor import PositionXpathProcessor
from app.xpath_processors.title_processor import TitleXpathProcessor
from app.xpath_processors.zhihu_processor import ZhiHuXpathProcessor

executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers based on your needs


async def fetch_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 禁用图片和视频加载
        await page.route("**/*.{png,jpg,jpeg,webp,mp4,webm,ogg}", lambda route: route.abort())

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            # 获取 HTML 内容
            content = await page.content()

        except TimeoutError:
            # 如果超时，返回 None
            content = None

        # 关闭浏览器
        await browser.close()

        return content


async def process_articles(config: Dict, document: etree._Element, html_content: Optional[str] = None) -> SiteNews:
    parameter = config['articleXpath'].get('parameter', 'default')
    if parameter == "position":
        return PositionXpathProcessor().analyzing_articles(config, document)
    elif parameter == "title":
        return TitleXpathProcessor().analyzing_articles(config, document)
    elif parameter == "zhihu":
        if html_content is None:
            raise ValueError("HTML content must be provided for ZhiHuXpathProcessor")
        return ZhiHuXpathProcessor().analyzing_articles(config, document, html_content)
    else:
        processor = DefaultXpathProcessor()
        return processor.analyzing_articles(config, document)
