"""this program returns info about articles(with body) from tproger.ru"""

from json import dumps
import itertools

import requests
from lxml import html


def get_article_info(url: str):
    """returns info about a article"""
    response = requests.get(url)
    page = html.fromstring(response.content)

    return {
        'url': url,
        'title': page.xpath('//h1[contains(@class,"title")]/text()')[0],
        'body': ''.join(page.xpath(
            '//div[contains(@itemprop, "articleBody")]/*[not(div)]/text()')
        ).strip().replace('\n', ''),
        'images':  page.xpath('//noscript/img[contains(@class,"size-full")]/@src | //noscript/img[contains(@class,"image-tool")]/@src'),
        'datePublished': page.xpath('//div[contains(@class, "post-meta")]/ul/li/time/@datetime')[0],
    }


def get_articles_info_from_pages(page_count: int):
    """returns list of info about articles """
    links = []

    for counter in range(page_count):
        response = requests.get('https://tproger.ru/page/%s/' % (counter+1))
        page = html.fromstring(response.content)
        links.append(page.xpath(
            '//article[contains(@class, "category-articles") or contains(@class, "category-translation") or contains(@class,"category-interview")]/a/@href'))
    links = list(itertools.chain.from_iterable(links))

    return [get_article_info(link) for link in links]


def main():
    """entry point of program"""
    with open('result.json', mode='wt') as f:
        for blog in get_articles_info_from_pages(3):
            print(dumps(blog, indent=2, ensure_ascii=False), file=f)


if __name__ == '__main__':
    main()
