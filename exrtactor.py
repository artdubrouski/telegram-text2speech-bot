import aiohttp
from boilerpy3 import extractors


extractor = extractors.ArticleExtractor()


async def url_extractor(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as response:
            content = await response.text()
            article = extractor.get_content(content)
            return article
