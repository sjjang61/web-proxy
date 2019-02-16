# -*- coding: utf-8 -*-
import sys
import logging.handlers

# http://docs.python-requests.org/en/latest/user/quickstart/
from const import Const
from httpClient import HttpClient

from flask import Flask, jsonify
from flask import render_template
from flask import request, json
from bs4 import BeautifulSoup

# For Python3
import urllib.request
import urllib.parse
from urllib.parse import urlparse

app = Flask(__name__, static_url_path='/static' )
logger = logging.getLogger("pparisa")


def urlencode(str):
  return urllib.parse.quote(str)

def urldecode(str):
  return urllib.parse.unquote(str)

#------------ HTML --------------#
@app.route('/', methods=['GET'])
def index():
    return render_template( 'index.html' )


@app.route('/webproxy', methods=['GET'])
def output():
    url = request.args.get("url")
    return render_template('proxy.html', req={'url': url })


#------------ API --------------#
@app.route('/proxy/', methods=['GET'])
def proxyHttp():
    url = request.args.get("url")
    return proxy(url)


@app.route('/proxyAjax', methods=['POST', 'GET'])
def proxyAjax():
    orig_url = request.args.get("orig_url")
    orig_path = request.args.get("orig_path")
    print( "[ajax] url = %s, path = %s" % ( orig_url, orig_path ) )

    if str(orig_url).startswith( 'about:' ):
        print("[ajax] no data")
        return '<!-- NO DATA -->'

    # . 으로 시작할경우, 제거
    if orig_path[0] == '.':
        orig_path = orig_path[1:]

    url = ""
    if str(orig_path).startswith("http://"):
        url = orig_path
    elif str(orig_url).startswith('://'):
        url = 'http' + orig_url
    else:
        url = orig_url + orig_path

    # 헤더추가 이슈 : https://sarc.io/index.php/development/806-python-html-contents-file-http-error-403-forbidden
    httpclient = HttpClient( url )
    headers = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181',
        'Referer': orig_url
    }
    content = httpclient.requestUrl(url, headers)

    if str(orig_path).startswith( '/pub/blog.html' ):
        print("[blog1] ===> ", url )
        # print("[blog2] ", content )

    return content

@app.route('/proxyIframe', methods=['GET'])
def proxyIframe():

    orig_url = request.args.get("orig_url")
    print( "[iframe] url = ", urldecode( orig_url) )
    # about:blank, about://blank?
    if str(orig_url).startswith( 'about:' ):
        # print("no data")
        return '<!-- NO DATA -->'

    if str(orig_url).startswith( '://' ):
        orig_url = 'http' + orig_url
        print("no protocol = ", orig_url)


    httpclient = HttpClient(orig_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181',
        'Referer': orig_url
    }
    content = httpclient.requestUrl(urldecode( orig_url), headers)
    return content + Const.AJAX_HOOKING_SCRIPT_CODE


def proxy( url ):

    host = urlparse(url).hostname
    protocol = urlparse(url).scheme
    # logger.debug( "[REQ] URL = %s, HOST = %s, Protocol = %s " % (url, host, protocol))

    headers = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181'
    }

    # 헤더추가 이슈 : https://sarc.io/index.php/development/806-python-html-contents-file-http-error-403-forbidden
    httpclient = HttpClient(url)
    content = httpclient.requestUrl(url, headers)
    # content = requestUrl(url, headers)
    soup = BeautifulSoup(content, 'lxml')

    # script, iframe 기능 제거
    # [s.extract() for s in soup('script')]
    # [s.extract() for s in soup('iframe')]

    # iframe src 변경 (proxyIframe 으로 변경)
    frameList = soup.select('iframe')
    for frame in frameList:
        frameUrl = frame.get('src')

        # if str(frameUrl).startswith('://'):
        #     frameUrl = 'http' + frameUrl
        # elif str(frameUrl).startswith('//'):
        #     frameUrl = 'http:' + frameUrl

        if frameUrl is not None:
            print("[iframe] url = ", frameUrl)

            # print("iframe url encoding = ", urlencode( frameUrl ))
            path = urlparse(frameUrl)
            print(path)
            orig_url = "%s://%s%s?%s" % (path.scheme, path.netloc, path.path, urlencode(path.query))
            frame.attrs['src'] = "/proxyIframe?orig_url=" + orig_url

    # css link change
    cssList = soup.select('link')
    for css in cssList:
        cssUrl = css.get('href')
        if css.get('rel')[0] == 'stylesheet' and cssUrl.startswith('/') and cssUrl.startswith('//') == False:
            css.attrs['href'] = protocol + '://' + host + cssUrl
            # print( css.get( 'href' )  )

    # img link change
    imgList = soup.select('img')
    for img in imgList:
        imgUrl = img.get('src')
        # if imgUrl.startswith('/') and imgUrl.startswith('//') :
        #     img.attrs['src'] = protocol + '://' + host + imgUrl
            # print( img.get( 'src' )  )

    if soup.find('title') is not None:
        logger.debug("[RES] TITLE = %s " % (soup.find('title').text))

    # return Const.HTML_BODY_PREFIX + str(soup) + Const.EXTRA_SCRIPT_CODE + Const.HTML_BODY_SUFFIX
    # html = str(soup).replace( 'document.domain = "naver.com"', 'document.domain = "localhost";')
    return Const.HTML_BODY_PREFIX + str(soup) + Const.AJAX_HOOKING_SCRIPT_CODE + Const.HTML_BODY_SUFFIX


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
