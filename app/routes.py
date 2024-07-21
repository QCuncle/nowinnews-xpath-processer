import time

import asyncio
from bs4 import BeautifulSoup
from flask import current_app as app
from flask import request, jsonify
from lxml import html

from app.models import SiteNews
from app.utils import process_articles, fetch_html


@app.route('/xpath/process', methods=['POST'])
async def xpath_process():
    xpath_list = request.get_json()

    async def process_item(item):
        url = item.get('siteUrl')
        html_content = await fetch_html(url)

        if not html_content:
            return SiteNews(
                siteCode=item.get('code'),
                siteName=item.get('name'),
                siteIconUrl=item.get('siteIconUrl'),
                updateTimestamp=int(time.time() * 1000),
                data=[]
            )
        else:
            try:
                # Use BeautifulSoup to parse and clean the HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                cleaned_html = str(soup)
                # Parse the cleaned HTML with lxml
                tree = html.fromstring(cleaned_html)
                print(item.get('code'))
                articles = await process_articles(item, tree, html_content)
                return articles
            except Exception | TimeoutError as e:
                return SiteNews(
                    siteCode=item.get('code'),
                    siteName=item.get('name'),
                    siteIconUrl=item.get('siteIconUrl'),
                    updateTimestamp=int(time.time() * 1000),
                    data=[]
                )

    tasks = [process_item(item) for item in xpath_list]
    results = await asyncio.gather(*tasks)

    return jsonify(results)
