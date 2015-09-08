# -*- coding: utf-8 -*-

import urllib2
import json

class SendMessage:

    def PostMessage(self):
        appid="wx1ba732a93b9bf1ce"#"wx6c07cc4b6bf2f472"
        secret="452074ad310735ab3167b4c64d10e27c"#"8ed8b3230860781ee619e31fc7c37309"
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret
        response = urllib2.urlopen(url)
        html = response.read()
        tokeninfo = json.loads(html)
        token=tokeninfo['access_token']
        post='''
{
   "touser":[
    "ogEIiwpNPRxOu7_TS91fG3XBC2ps"
   ],
    "msgtype": "text",
    "text": { "content": "hello from boxer."}
}'''
        url = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=' + token
        req = urllib2.Request(url, post)
        response = urllib2.urlopen(req)
        html = response.read()
        tokeninfo = json.loads(html)
        return tokeninfo