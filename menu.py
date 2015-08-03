# -*- coding: utf-8 -*-
import sae
import web
import xml.etree.ElementTree as ET
import sae.const
import MySQLdb
import urllib2
import json

class CreatMenu:

    def GET(self):
        appid="wx6c07cc4b6bf2f472"
        secret="8ed8b3230860781ee619e31fc7c37309"
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret
        response = urllib2.urlopen(url)
        html = response.read()
        tokeninfo = json.loads(html)
        token=tokeninfo['access_token']
        post='''
 {
     "button":[
     {	
          "type":"click",
          "name":"视频",
          "key":"http://v.qq.com/"
      },
      {
           "type":"click",
           "name":"音乐",
           "key":"V1001_TODAY_MUSIC"
      },
      {
          "type":"view",
           "name":"help",
           "key":"http://www.shidou.com/"
       }]
 }'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+token
        req = urllib2.Request(url, post.encode("utf-8"))
        response = urllib2.urlopen(req)
        html = response.read()
        tokeninfo = json.loads(html)
        return tokeninfo, token