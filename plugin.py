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
import json

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

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

        search_url = 'http://packagist.org/search.json'
        opts = { 'q' : text }

	url = '%s?%s' % ( search_url, urllib.urlencode( opts ) )
        fd = utils.web.getUrlFd( url, headers )
	result = json.load( fd )
        fd.close()

	if len(result) > 0 and result[ 'total' ] > 0:
          s = '%d matches: ' % ( result[ 'total' ] )
          matches = []
          for i in result[ 'results' ]:
            matches.append( '%s: %s <%s>' % ( i[ 'name' ], i[ 'description' ], i[ 'url' ] ) )
	  s += ' | '.join(matches)
          irc.reply(s)
        else:
           irc.reply( 'No Matches' )
    find = wrap(find, ['text'])


Class = Packagist


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
