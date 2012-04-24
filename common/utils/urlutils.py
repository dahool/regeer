# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import re
import urllib
import urlparse

from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import smart_str, force_unicode
from django.utils.functional import allow_lazy

# Configuration for urlize() function.
TRAILING_PUNCTUATION = ['.', ',', ':', ';']
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('&lt;', '&gt;')]

# List of possible strings used for bullets in bulleted lists.
DOTS = [u'&middot;', u'*', u'\u2022', u'&#149;', u'&bull;', u'&#8226;']

unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
unquoted_percents_re = re.compile(r'%(?![0-9A-Fa-f]{2})')
word_split_re = re.compile(r'(\s+)')
simple_url_re = re.compile(r'^https?://\w', re.IGNORECASE)
simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$', re.IGNORECASE)
simple_email_re = re.compile(r'^\S+@\S+\.\S+$')
link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')

from django.utils.html import escape

def extract_params(data):
    try:
        url, params = data.split('?')
    except ValueError:
        return (data, {})
    return (url, parse_params(params))

def parse_params(data):
    pdic = {}
    for elem in data.split('&'):
        key, value = elem.split('=')
        pdic[key] = value
    return pdic

def serialize_params(data):
    return urllib.urlencode(data)

# this doesn't exists in django prior to django 1.4
def smart_urlquote(url):
    "Quotes a URL if it isn't already quoted."
    # Handle IDN before quoting.
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    try:
        netloc = netloc.encode('idna') # IDN -> ACE
    except UnicodeError: # invalid domain part
        pass
    else:
        url = urlparse.urlunsplit((scheme, netloc, path, query, fragment))

    # An URL is considered unquoted if it contains no % characters or
    # contains a % not followed by two hexadecimal digits. See #9655.
    if '%' not in url or unquoted_percents_re.search(url):
        # See http://bugs.python.org/issue2637
        url = urllib.quote(smart_str(url), safe='!*\'();:@&=+$,/?#[]~')

    return force_unicode(url)

def urlize(text, replaceText, target=False, nofollow=False, autoescape=False):
    """
    This code is taken from django, but it allows to replace the text
    instead of using the original url
    
    Converts any URLs in text into clickable links.

    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.

    If nofollow is True, the URLs in link text will get a rel="nofollow"
    attribute.

    If autoescape is True, the link text and URLs will get autoescaped.
    """
    safe_input = isinstance(text, SafeData)
    words = word_split_re.split(force_unicode(text))
    for i, word in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word:
            # Deal with punctuation.
            lead, middle, trail = '', word, ''
            for punctuation in TRAILING_PUNCTUATION:
                if middle.endswith(punctuation):
                    middle = middle[:-len(punctuation)]
                    trail = punctuation + trail
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead = lead + opening
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing)
                    and middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail

            # Make URL we want to point to.
            url = None
            nofollow_attr = ' rel="nofollow"' if nofollow else ''
            if target:
                nofollow_attr = ' target="_blank"'
            if simple_url_re.match(middle):
                url = smart_urlquote(middle)
            elif simple_url_2_re.match(middle):
                url = smart_urlquote('http://%s' % middle)
            elif not ':' in middle and simple_email_re.match(middle):
                local, domain = middle.rsplit('@', 1)
                try:
                    domain = domain.encode('idna')
                except UnicodeError:
                    continue
                url = 'mailto:%s@%s' % (local, domain)
                nofollow_attr = ''

            # Make link.
            if url:
                if autoescape and not safe_input:
                    lead, trail = escape(lead), escape(trail)
                    url, replaceText = escape(url), escape(replaceText)
                middle = '<a href="%(url)s" title="%(url)s"%(attr)s>%(text)s</a>' % {'url': url, 
                                                                                     'attr': nofollow_attr,
                                                                                     'text': replaceText}
                words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
            else:
                if safe_input:
                    words[i] = mark_safe(word)
                elif autoescape:
                    words[i] = escape(word)
        elif safe_input:
            words[i] = mark_safe(word)
        elif autoescape:
            words[i] = escape(word)
    return u''.join(words)
urlize = allow_lazy(urlize, unicode)
