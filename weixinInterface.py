# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json,urllib
import httplib
from lxml import etree
import pylibmc
import random

class WeixinInterface:
    
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.replayText = [u'欢迎关注本公众号，请输入help查看所有功能',
                           u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来',
                           u'''这是本人业余开发的订阅号，做得不够好请见谅，快回复数字菜单或者输入关键字进入对应功能体验一下吧……
1.翻译(输入中文或者英文)
2.听音乐（关键字m）
3.公司官网（关键字l）
4.未完待续'''
                           
                           ]
        self.musicList = [
                          [r'http://play.baidu.com/?__m=mboxCtrl.playSong&__a=266922&__o=song/266922||playBtn&fr=-1||www.baidu.com#','百度随心听',u'请点击进入网页播放'] , 
                          [r'http://testengineer-music.stor.sinaapp.com/%E6%B7%B1%E5%A4%9C%E5%9C%B0%E4%B8%8B%E9%93%81.mp3','深夜地下铁',u'献给我的肠粉们']
                          ]
        self.htmlList = [
                         [r'http://www.shidou.com','shidou',u'公司官网','http://testengineer-picture.stor.sinaapp.com/20150715151456.jpg']
                         ]

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="testengineer" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        mstype=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作

        #下面创建一个欢迎消息，通过判断Event类型
        if mstype == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[0])
            if mscontent == "unsubscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[1])
        if mstype == 'text':
            content=xml.find("Content").text
            if content == 'help':
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[2])
            elif content.lower() == 'm' or content == '2':
                music = random.choice(self.musicList)
                return self.render.reply_music(fromUser,toUser,int(time.time()),music[1],music[2],music[0])
            elif content.lower() == 'l' or content == '3':
                html = random.choice(self.htmlList)
                return self.render.reply_news(fromUser, toUser, int(time.time()), html[1], html[2], html[0], html[3])
            else :
                if type(content).__name__ == "unicode":
                    content = content.encode('utf-8')
                Nword = self.youdao(content)
                return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)

    def youdao(self, word):
        qword = urllib2.quote(word)
        baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=testengineer&key=1824780031&type=data&doctype=json&version=1.1&q='
        url = baseurl+qword
        try:
            resp = urllib2.urlopen(url)
            fanyi = json.loads(resp.read())
        except urllib2.HTTPError, e:
            return "urllib2 http error:", str(e.code), ":", str(e.reason), str(e)
        except urllib2.URLError, e:
            return "urllib2 URL error:", e.message
        except httplib.HTTPException, e:
            return "urllib2 URL error:", e.message
        except:
            return "unknown error"

        if fanyi['errorCode'] == 0:
            if 'basic' in fanyi.keys():
                trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
                return trans
            else:
                trans =u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))
                return trans
        elif fanyi['errorCode'] == 20:
            return u'对不起，要翻译的文本过长'
        elif fanyi['errorCode'] == 30:
            return u'对不起，无法进行有效的翻译'
        elif fanyi['errorCode'] == 40:
            return u'对不起，不支持的语言类型'
        else:
            return u'对不起，您输入的单词%s无法翻译,请检查拼写'% word
