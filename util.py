#!/usr/bin/env python
import string
import random
import datetime
from datetime import tzinfo
import operator
import time
import urllib2
urlopen = urllib2.urlopen
import StringIO
import gzip
import cookielib
import datastream

def ds(str):
    # Convert string into data stream
    return datastream.DataStream(str)

def post(url, data):
    # This function for making post request
	import urllib
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	request.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)")
	request.add_data(data)
	rtn = opener.open(request)
	return rtn.read()


def readurl(url, cookie=None):
    # This function for making get request
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)")

    if cookie:
        request.add_header('Cookie', cookie)

    rtn = opener.open(request)

    if rtn.headers.dict.has_key('content-encoding') and rtn.headers.dict['content-encoding'] == 'gzip':
        cs = StringIO.StringIO(rtn.read())
        gzipper = gzip.GzipFile(fileobj=cs)
        data = gzipper.read()
        return data
    else:
        return rtn.read()

def readurl_simple(url):
    # This function is simple version for making a request
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    response = opener.open(url)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = cStringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        src = f.read()
    else:
        src = response.read()

    return src

#----------------------------------------------------------#
# proxies = [
#     "",
#     "IP_ADDRESS:PORT",
#     "IP_ADDRESS:PORT"
# ];
#
# request_count = 0
#----------------------------------------------------------#
def readurl_proxies(url, proxies, request_count):
    # This function is for making a request with proxies, request count
    opener = urllib2.OpenerDirector()
    opener.add_handler(urllib2.HTTPHandler(debuglevel=0))
    opener.add_handler(urllib2.HTTPSHandler(debuglevel=0))
    opener.add_handler(urllib2.HTTPRedirectHandler())

    pa = proxies[request_count % len(proxies)]
    proxy_handler = None
    if pa:
        proxy_handler = urllib2.ProxyHandler({'http': pa})
        print "pa:", pa
        opener.add_handler(proxy_handler)

    opener.addheaders += [('Accept-Encoding', "gzip")]

    response = opener.open(url)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = cStringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        src = f.read()
    else:
        src = response.read()
    request_count += 1
    return src

def readheader(url):
    # This function is for making a request to read header information
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    rtn = opener.open(request)
    return rtn.headers.dict	

def readurl_auth(uri, url, protocol, usr, pas, realm):
    # This function is for making a request with authentication information
    passman = urllib2.HTTPPasswordMgr()
    passman.add_password(realm, uri, usr, pas)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    return urllib2.urlopen(protocol + url).read()

def readurlssl(url):
    # This function is for making a request using ssl protocal
    cj = cookielib.LWPCookieJar("cookie")
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPSHandler(debuglevel=0),urllib2.HTTPCookieProcessor(cj))
    req = opener.open(url)
    return req.read()

def replace_html_symbol(src):
    # This function is for replacing special charater with human readable character
    src = string.replace(src, "&amp;", "&")
    src = string.replace(src, "&quot", "\"")
    src = string.replace(src, "&lt", "<")
    src = string.replace(src, "&gt", ">")
    src = string.replace(src, "&apos;", "'")
    src = string.replace(src, "(Neutral Venue)", "")

    src = string.replace(src, "&nbsp;", " ")
    src = string.replace(src, "&nbsp", " ")
    
    src = string.replace(src, '\xc3\x9f', "s")
    src = string.replace(src, '\xc3\xbc', "u")
    
    src = string.replace(src, '\x6f\xbc', "u")
    src = string.replace(src, '\xc3\xbc', "u")
    src = string.replace(src, '\xc3\xb9', "u")
    src = string.replace(src, '\xb6\xc3', "o")
    src = string.replace(src, '\xc2\xb4', "'")
    
    src = string.replace(src, '\xa4\xc3', "a")
    
    src = string.replace(src, '\xc3\x98', "o")
    src = string.replace(src, '\xc3\x9c', "U")
    src = string.replace(src, '\xc3\xa0', "a")
    src = string.replace(src, '\xc3\xa1', "a")
    src = string.replace(src, '\xc3\xa4', "a")
    src = string.replace(src, '\xc3\xa3', "a")
    src = string.replace(src, '\xc3\xa6', "ae")
    src = string.replace(src, '\xc3\xa8', "e")
    src = string.replace(src, '\xc3\xa9', "a")
    src = string.replace(src, '\xc3\xb3', "o")
    src = string.replace(src, '\xc3\xb6', "o")
    src = string.replace(src, '\xc3\xb8', "o")
    src = string.replace(src, '\xc3\xba', "u")
    src = string.replace(src, '\xc5\x84', "n")
    src = string.replace(src, '\xc5\x99', "r")
    src = string.replace(src, '\xc5\x99', "r")
    src = string.replace(src, '&#235;', "e")
    src = string.replace(src, '&#252;', "u")
    src = string.replace(src, '&#246;', "o")
    src = string.replace(src, '&#233;', "e")
    
    return src

def random_string(size):
    # This function is for generating random string with given size
    allowed = string.ascii_letters # add any other allowed characters here 
    randomstring = ''.join([allowed[random.randint(0, len(allowed) - 1)] for x in xrange(size)]) 
    return randomstring

def convert_date_string_into_timestamp(date_string):
    # This function is for convert date in string to "01/30/2011" format
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

def convert_date_string_into_timestamp_with_format(date_string, string_format):
    return time.mktime(datetime.datetime.strptime(date_string, string_format).timetuple())

if __name__ == "__main__":
    d = ds("-23dsdfa")
    a = d.readint()
    print a
