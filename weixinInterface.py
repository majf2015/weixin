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
                replayText = u'''欢迎关注本公众号，这个是本人业余爱好所建立，也是想一边学习Python一边玩的东西
        现在还没有什么功能，只是弄了个翻译与豆瓣图书查询的小工具，你们有什么好的文章也欢迎反馈给我,我会不定期的分享给大家，输入help查看操作指令'''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            if mscontent == "unsubscribe":
                replayText = u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
        if mstype == 'text':
            content=xml.find("Content").text
            if content == 'help':
                replayText = u'''1.输入中文或者英文返回对应的英中翻译
2.输入 book 要查询的书名 返回豆瓣图书中结果
3.输入cls清除查询记录
4.输入m随机来首音乐听，建议在wifi下听
5.输入python 进入python常用模块用法查询（未完成）'''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            if content.lower() == 'm':
                musicList = [ 
                             [r'http://play.baidu.com/?__m=mboxCtrl.playSong&__a=266922&__o=song/266922||playBtn&fr=-1||www.baidu.com#','百度随心听',u'献给我的肠粉们'] , 
                             [r'http://pan.baidu.com/s/1gdEn1CZ','深夜地下铁',u'请在wifi时下载']
                             ]
                music = random.choice(musicList)
                musicurl = music[0]
                musictitle = music[1]
                musicdes =music[2]
                return self.render.reply_music(fromUser,toUser,int(time.time()),musictitle,musicdes,musicurl)
            if content.lower() == 'l':
                htmlList = [r'http://www.shidou.com','shidou',u'公司官网']
                htmlurl = htmlList[0]
                htmltitle = htmlList[1]
                htmldes = htmlList[2]
                return self.render.reply_url(fromUser,toUser,int(time.time()),htmltitle,htmldes,htmlurl)
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
            print "query string:", url
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
