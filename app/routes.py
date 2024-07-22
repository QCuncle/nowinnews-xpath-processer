from bs4 import BeautifulSoup
from flask import current_app as app
from flask import request, jsonify
from lxml import html

from app.utils import process_articles, fetch_html


@app.route('/xpath/process', methods=['POST'])
async def xpath_process():
    item = request.get_json()

    url = item.get('siteUrl')
    html_content = await fetch_html(url)

    site_code = item.get('code')
    if not html_content:
        return jsonify({"code": -1, "message": site_code + "query failed", "data": {}})
    else:
        try:
            # Use BeautifulSoup to parse and clean the HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            cleaned_html = str(soup)
            # Parse the cleaned HTML with lxml
            tree = html.fromstring(cleaned_html)
            site_news = await process_articles(item, tree, html_content)
            return jsonify({"code": 0, "message": "successful", "data": site_news})
        except Exception | TimeoutError as e:
            return jsonify({"code": -1, "message": site_code + "timeout", "data": {}})
