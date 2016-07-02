#coding=utf-8
import urllib2
from cookie_util import IpProxy
class ProxyMiddleware(object):
    handle_httpstatus_list = [302, 403, 400, 401, 404, 500, 501, 502,504]

    def __init__(self):
        self.ip = self.get_ip()

    def process_request(self, request, spider):
        if 'mp.weixin.qq.com' in request.url:
            pass
        else:
            request.meta["dont_redirect"] = True
            request.meta['proxy'] = 'http://%s' % self.ip

    def process_response(self, request, response, spider):
         if response.status in self.handle_httpstatus_list:
             self.ip = self.get_ip()
             return request
         elif u'您的访问过于频繁' in response.body:
             self.ip = self.get_ip()
             return request
         else:
             return response

    def get_ip(self):
        try:
            req = urllib2.Request('http://127.0.0.1:8080/getIp?type=qunar')
            opener=urllib2.build_opener()
            urllib2.install_opener(opener)
            response = opener.open(req)
            ip = response.read()
            return ip
        except Exception, e:
            print e
            return None