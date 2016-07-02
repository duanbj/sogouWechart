#coding=utf-8
import urllib2
from time import sleep
import threading
import random
import logging
import cookielib
class IpProxy():
    # 去哪儿网代理池
    proxy_qunar = []
    # 艺龙ip代理池
    proxy_elong = []
    # 携程ip代理池
    proxy_ctrip = []
    proxy_sogou = []
    url_quanr = 'http://www.sogou.com/'
    url_ctrip = 'http://www.sogou.com/'
    url_elong = 'http://www.sogou.com/'
    url_wehcart = 'http://weixin.sogou.com/weixin?type=2&query=python&ie=utf8&_sug_=n&_sug_type_='
    sogou_cookie = []
    logger = logging.getLogger('django')

    @staticmethod
    def start():
        thread = threading.Thread(target=IpProxy.get_ip_thread)
        thread.setDaemon(True)
        thread.start()
        v_ip_thread = threading.Thread(target=IpProxy.v_ip_thread)
        v_ip_thread.setDaemon(True)
        v_ip_thread.start()

    @staticmethod
    def get_cookie():
        return random.choice(IpProxy.sogou_cookie)


    @staticmethod
    def get_ip_thread():
        while True:
            url_kuaidaili = 'http://dev.kuaidaili.com/api/getproxy/?orderid=976589578932029&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&f_loc=1&f_pr=1&f_sp=1&quality=1&sort=1&sep=1'
            url_daili666 = 'http://qsrdk.daili666api.com/ip/?tid=557950053076024&num=100&category=2&delay=1&longlife=20'
            IpProxy.get_ip(url_kuaidaili, 1)
            IpProxy.get_ip(url_daili666, 2)

    @staticmethod
    #代理ip验证
    def v_ip_thread():
        while True:
            for ip in IpProxy.proxy_sogou:
                if IpProxy.proxy_identify(ip, IpProxy.url_wehcart):
                    pass
                else:
                    try:
                        IpProxy.logger.info('ctrip:删除ip %s' % ip)
                        IpProxy.proxy_sogou.remove(ip)
                    except Exception, e:
                        print e
            sleep(10)

    @staticmethod
    def get_ip(url,type):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            ips = response.read()
            l = []
            if type == 1:
                l = ips.split("\n")
            else:
                l = ips.split("\r\n")
            response.close()
            for ip in l:
                ip = ip.split(',')[0]
                if IpProxy.proxy_identify(ip, IpProxy.url_wehcart) and IpProxy.proxy_sogou.count(ip) == 0:
                    IpProxy.proxy_sogou.append(ip)
                    IpProxy.logger.info('qunar:%s,len:%s' %(ip, str(len(IpProxy.proxy_sogou))))
        except Exception, e:
            print '获取代理ip异常！ %s' %e
            sleep(30)

    @staticmethod
      # 验证代理ip有效性
    def proxy_identify(proxy, url):
        cookie = cookielib.LWPCookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        proxy_support = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_support, handler)
        try:
            response = opener.open(url, timeout=3)
            if response.code == 200:
                c = ''
                for item in cookie:
                    c += item.name+'='+item.value+';'
                print c
                IpProxy.sogou_cookie.append(c)
                return True
        except Exception, error:
            print error
            return False


if __name__ == '__main__':
   IpProxy.start()