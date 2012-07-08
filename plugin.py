###
# Copyright (c) 2012, Kevin Boyd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import urllib

from HTMLParser import HTMLParser

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

class MyParser(HTMLParser):
  def __init__(self, irc):
    HTMLParser.__init__(self)
    self.items = {}
    self.current_item = None
    self.current_description = False
    self.current_link = False

  def handle_starttag(self, tag, attrs):
    if tag == 'li' and attrs[0][0] == 'data-url':
      self.current_item = attrs[0][1]
      self.items[ self.current_item ] = {}
      self.items[ self.current_item ][ 'data-url' ] = attrs[0][1]

    if tag == 'a' and self.current_item != None:
      self.current_link = True

    if tag == 'p' and self.current_item != None and attrs[0] == ( 'class', 'package-description' ):
      self.current_description = True

  def handle_endtag(self, tag):
    if tag == 'a':
      self.current_link = False
    if tag == 'p':
      self.current_description = False

  def handle_data(self, data):
    if self.current_link is True:
      self.items[ self.current_item ][ 'name' ] = data
    if self.current_description is True:
      self.items[ self.current_item ][ 'desc' ] = data

  def PrintItems(self, irc):
    s = '%d matches' % ( len(self.items) )
    s += ': '
    matches = []
    for i in self.items:
      matches.append( '%s: %s <http://packagist.org%s>' % ( self.items[i]['name'], self.items[i]['desc'], self.items[i]['data-url'] ) )
    s += " | ".join(matches)
    irc.reply(s)
    
class Packagist(callbacks.Plugin):
    """Packagist plugin lets you search http://packagist.org for Composer
    packages
    - the @find <keyword> command is used to peform searches"""
    threaded = True
    def find(self, irc, msg, args, text):
        """<keyword>

        Searches http://packagist.org for Composer packages that match <keyword>
        """
        headers = utils.web.defaultHeaders
        headers['X-Requested-With'] = 'XMLHttpRequest'

        search_url = 'http://packagist.org/search/'
        opts = { 'search_query[query]' : text }

        fd = utils.web.getUrlFd( '%s?%s' % (search_url, urllib.urlencode(opts)), headers )
        parser = MyParser(irc)
        parser.feed(fd.read())
        parser.PrintItems(irc)
        fd.close()
    find = wrap(find, ['text'])


Class = Packagist


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
