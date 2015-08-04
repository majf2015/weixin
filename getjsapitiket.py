# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import urllib2
import json

class GetJsapiTicket:
    def __init__(self):
        self.appid ="wx6c07cc4b6bf2f472"
        self.secret ="8ed8b3230860781ee619e31fc7c37309"
        self.urlapi ='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+self.appid+'&secret='+self.secret
        self.urltoken = 'http://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token='
        self.urlhtml = 'http://play.baidu.com/?__m=mboxCtrl.playSong&__a=266922&__o=song/266922||playBtn&fr=-1||www.baidu.com#'

    def GET(self):
        response = urllib2.urlopen(self.urlapi)
        html = response.read()
        tokeninfo = json.loads(html)
        token_token=tokeninfo['access_token']
        req = urllib2.Request(self.urltoken + token_token)
        response = urllib2.urlopen(req)
        html = response.read()
        tokeninfo = json.loads(html)
        jsapi_ticket = tokeninfo['jsapi_ticket']
        return jsapi_ticket, self.urlhtml