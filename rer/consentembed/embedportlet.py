# -*- coding: utf-8 -*-

import re
from collective.portlet.embed.portlet import Renderer as BaseRenderer
from pyquery import PyQuery as PQ
from rer.consentembed import logger
from plone.memoize import ram


DANGEROUS_EXPR = ("iframe[src],script[src],"
                  "object[data],embed[src],"
                  "video source[src],audio source[src],"
                  "image[src],link[src]")

URL_PATTER = r"^[^a-zA-Z0-9]*(?:http://|https://)?([a-zA-Z0-9.:]+).*$"
urlmatcher = re.compile(URL_PATTER)


def _available_cachekey(method, self):
    return self.data.text


class EmbedPortletRender(BaseRenderer):
    """Check if the portlet is trying to load data from external.

    If this is true, and a cookie named "embed-optout" is present with value "true"
    or the DNT header is provided, do not load the portlet.
    """

    @property
    def available(self):
        if self.request.cookies.get('embed-optout') != 'true' and \
                self.request.get_header('HTTP_DNT') != '1':
            return True

        return self._content_available_check()

    @ram.cache(_available_cachekey)
    def _content_available_check(self):
        # This only check HTML content, so can be cached
        text = self.data.text
        here_url = self.context.absolute_url()
        currentDomain = urlmatcher.match(here_url).groups()[0]
        
        try:
            pq = PQ(text)
        except:
            logger.error('Cannot parse portlet contents')
            return False

        items = pq.find(DANGEROUS_EXPR)
        for element in items.items():
            to_check = element.attr('src') or element.attr('data')
            remoteMatch = urlmatcher.match(to_check)
            if not remoteMatch:
                # not an URL, maybe not dangerous?
                continue
            if currentDomain!=remoteMatch.groups()[0]:
                return False
        return True
