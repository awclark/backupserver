
# Original open source found at https://gist.github.com/timss/5503221
# Edited by Angus Clark 4/4/2017

import html2text
import re
import sys
import urllib2

def get_ip(host):
    trac = "http://www.ip-adress.com/ip_tracer/"
    pat  = "ISP of this IP \[\?\]:\n\n([a-zA-Z ]+)"
    hdr  = {'User-Agent': 'Mozilla/5.0'} # ip-adress.com only accepts popular agents
    req  = urllib2.Request(trac + host, headers=hdr)
    page = urllib2.urlopen(req).read()

    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(page)

    try:
        return re.search(pat, text).group(1)
    except:
       	return 'NA'

