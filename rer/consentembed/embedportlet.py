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

URL_PATTER = r"^[^a-zA-Z0-9]*(?:http://|https://)?([a-zA-Z0-9.:_\-]+).*$"
urlmatcher = re.compile(URL_PATTER)


def _subdomain_cachekey(method, self, domain):
    return domain

def _available_cachekey(method, self):
    # Cache is based onto portlet contents and subdomain used by users to access the site
    here_url = self.context.absolute_url()
    currentDomain = urlmatcher.match(here_url).groups()[0]
    currentSubDomain = self._get_subdomain(currentDomain)
    return (self.data.text, currentSubDomain)


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

    @ram.cache(_subdomain_cachekey)
    def _get_subdomain(self, domain):
        """
        aaa.bbb.com -> bbb.com
        aaa.bbb.ccc.com -> bbb.com
        aaa.com -> aaa.com
        aaa -> aaa
        ip addr -> ip addr
        """
        # aaa
        if domain.find(".")==-1:
            return domain
        domain = domain.split(':')[0] # do not care about port
        parts = domain.split('.')
        # ip addr
        if len([x for x in parts if x.isdigit()]) == len(parts):
            return domain
        # aaa.com 
        if len(parts)<=2:
            return domain
        # other
        return '.'.join(parts[-2:])

    @ram.cache(_available_cachekey)
    def _content_available_check(self):
        # This only check HTML content, so can be cached
        text = self.data.text
        here_url = self.context.absolute_url()
        currentDomain = urlmatcher.match(here_url).groups()[0]
        currentSubDomain = self._get_subdomain(currentDomain)
        
        try:
            pq = PQ(text)
        except:
            logger.error('Cannot parse portlet contents')
            return False

        items = pq(DANGEROUS_EXPR)
        for element in items.items():
            to_check = element.attr('src') or element.attr('data')
            remoteMatch = urlmatcher.match(to_check)
            if not remoteMatch:
                # not an URL, maybe not dangerous?
                continue
            if remoteMatch.groups()[0].find(currentSubDomain)==-1:
                return False
        return True
