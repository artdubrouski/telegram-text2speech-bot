import aiohttp
import re

from boilerpy3 import extractors


extractor = extractors.ArticleExtractor()

pattern = r"(http|ftp|https|)?(://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"


async def url_extractor(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as response:
            content = await response.text()
            article = extractor.get_content(content)
            cleaned_article = await humanize_urls_in_text(article)
            return cleaned_article


async def humanize_urls_in_text(text):
    patt = re.compile(pattern)
    cleaned_text = re.sub(patt, lambda x: x.group(3).replace('www.', ''), text)
    return cleaned_text + '\n\nEND\n\nOF\n\nFILE \n\n'


async def is_url(string):
    if re.match(pattern, string):
        return True
    else:
        return False
