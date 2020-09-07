import logging
import aiohttp
import re
import settings

from boilerpy3 import extractors


extractor = extractors.ArticleExtractor()
pattern = r"(http|ftp|https|)?(://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
logger = logging.getLogger('article_bot')


async def extract_text_from_url(url: str) -> str:
    '''Returns article extracted by boilerpy3.'''
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(url) as response:
                content = await response.text()
                article = extractor.get_content(content)
                cleaned_article = await humanize_urls_in_text(article)
                return cleaned_article

        except aiohttp.ClientError as err:
            logger.warning(err)
            return ''


async def humanize_urls_in_text(text: str) -> str:
    '''Extracts domain part from the given URL.'''
    patt = re.compile(pattern)
    cleaned_text = re.sub(patt, lambda x: x.group(3).replace('www.', ''), text)
    return cleaned_text + settings.EOF_STRING


async def is_url(string: str) -> bool:
    '''Checks if the string is url-like.'''
    if re.match(pattern, string):
        return True
    else:
        return False
