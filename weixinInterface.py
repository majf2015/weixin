
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
import time


class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.replayText = [u'欢迎关注本公众号，请输入help查看所有功能',
                           u'您已退出help流程，如需进入重新输入help,或者直接对应输入关键字',
                           u'''业余开发，请见谅，回复数字或者输入关键字进入对应功能体验一下吧……
1.翻译(回复1/输入y)
2.听音乐（回复2/输入m）
3.个人主页（回复3/输入l）
4.美食教程（回复4/输入e）
5.文艺生活（回复5/输入a）
6.未完待续（回复6/输入exit）''',
                           u'欢迎使用翻译功能，请输入中文，或者英文进行翻译，如需返回help流程请输入“q”，如需返回默认状态请输入“exit”',
                           u'请输入对应的数据菜单，或者直接输入关键字',
                           u'你已退出翻译流程，目前在help流程下'

                           ]
        self.musicList = [
                          [r'http://fm.baidu.com/#','百度随心听',u'请点击进入网页播放'] ,
                          [r'http://music.163.com/#/song?id=295150','深夜地下铁',u'献给我的肠粉们']
                          ]
        self.newList = [
                         [u'简单网页', 'my web', 'http://pic16.nipic.com/20110918/3101644_091102012560_2.jpg', r'http://testengineer.sinaapp.com/web'],
                         [u'公司官网', 'shidou', 'http://img4.duitang.com/uploads/item/201111/21/20111121222741_TXe8h.thumb.600_0.jpg', r'http://www.shidou.com'],
                         [u'个人微博', 'wei bo', 'http://p2.img.cctvpic.com/nettv/newgame/cdn_pic/mzl.amvyqtlq.png', r'http://m.weibo.cn/u/3123503230?from=1054095010&wm=9848_0009&sourceType=qq&uid=3123503230'],
                         [u'QQ空间', 'QQ', 'http://pic.crsky.com/uploadfiles/2012-10-15/201210151552078456.png', r'http://user.qzone.qq.com/1021008546']
                         ]
        self.eatList = [
                         [u'香蕉煎饼', '助眠食谱', 'http://i3.meishichina.com/attachment/recipe/201110/201110261412563.jpg', r'http://home.meishichina.com/recipe-35763.html'],
                         [u'香蕉奶昔', '助眠食谱', 'http://i3.meishichina.com/attachment/recipe/2012/12/18/20121218170900738892789.jpg', r'http://home.meishichina.com/recipe-4187.html'],
                         [u'莲子鲜奶露', '助眠食谱', 'http://i3.meishichina.com/attachment/recipe/201110/201110171439004.jpg', r'http://home.meishichina.com/recipe-37820.html'],
                         [u'杏仁奶糊', '助眠食谱', 'http://i3.meishichina.com/attachment/recipe/201110/201110181412071.jpg', r'http://home.meishichina.com/recipe-37445.html']
                         ]
        self.artList = [
                         [u'若非心里有人，怎会暗里有光 ', '文艺生活', 'http://mmbiz.qpic.cn/mmbiz/HhorckbERhia8ickgSBiaib1ZoApHKJrEpdTk8KZ0bjk5kFIgLzobvCtelMgaHkuSD25ibtIcqPKydmTiczVnyic3gHBg/640?wx_fmt=jpeg&wxfrom=5', r'http://mp.weixin.qq.com/s?__biz=MjM5ODA0NTc4MA==&mid=212548048&idx=1&sn=127f38e95cdf1a61a534d4791905ebc9#rd'],
                         [u'远远走来一个绿茶女 ', '文艺生活', 'http://mmbiz.qpic.cn/mmbiz/HhorckbERhhTzbVQP4atncicBnCvLSQK3DgConeySrWcMp55wM2jKswcKHAr9L8icu0wfFqmr1MWnU7WItFJiaq5A/640?wx_fmt=jpeg&wxfrom=5', r'http://mp.weixin.qq.com/s?__biz=MjM5ODA0NTc4MA==&mid=212886080&idx=1&sn=85c7c46726d62214c7bb81f9a8952158#rd'],
                         [u'邮寄一只企鹅 ', '文艺生活', 'http://mmbiz.qpic.cn/mmbiz/HhorckbERhiabxfjhGrUTicq6BqXEY0EAsI6c4CJgzWM5spYsBKibdrtMO6F1Q504vZbiaLnicEnUMiakh4kuY8T5tMg/640?wx_fmt=jpeg&wxfrom=5', r'http://mp.weixin.qq.com/s?__biz=MjM5ODA0NTc4MA==&mid=213047416&idx=1&sn=7afc95e80fa51ad274401d02a855973a&scene=0#rd'],
                         [u'只是因为在泳池中多看了你一眼 ', '文艺生活', 'http://mmbiz.qpic.cn/mmbiz/HhorckbERhgrXI6k47PjicddcKiaz2b5uh4IJcCCvq7f0KBUSLyBuzhEILVLpDElYEtZORakPHice32BtsZFH4a8w/640?wx_fmt=jpeg&wxfrom=5', r'http://mp.weixin.qq.com/s?__biz=MjM5ODA0NTc4MA==&mid=213226719&idx=1&sn=8aff79da49f2de9b29743931077738ed&scene=0#rd']
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
        self.mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作
        if not self.mc.get(fromUser):
            self.mc.set(fromUser, 'exit')


        #下面创建一个欢迎消息，通过判断Event类型
        if mstype == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[0])
            if mscontent == "unsubscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[1])
        if mstype == 'text':
            content=xml.find("Content").text
            if self.mc.get(fromUser) == 'help':
                if content == '1' or content == 'y':
                    content = 'y'
                elif content == '2' or content == 'm':
                    content = 'm'
                elif content == '3' or content == 'l':
                    content = 'l'
                elif content == '4' or content == 'e':
                    content = 'e'
                elif content == '5' or content == 'a':
                    content = 'a'
                elif content == '6' or content == 'exit':
                    content = 'exit'
                else:
                    content = 'else'



            if content == 'help':
                self.mc.set(fromUser, 'help')
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[2])
            elif content.lower() == 'exit':
                self.mc.set(fromUser, 'exit')
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[1])
            elif content.lower() == 'else':
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[4])
            elif content.lower() == 'q':
                self.mc.set(fromUser, 'help')
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[5])
            elif content.lower() == 'y':
                self.mc.set(fromUser, 'fanyi')
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[3])
            elif content.lower() == 'm':
                music = random.choice(self.musicList)
                return self.render.reply_music(fromUser,toUser,int(time.time()),music[1],music[2],music[0])
            elif content.lower() == 'l':
                return self.render.reply_news(fromUser, toUser, int(time.time()), self.newList[0], self.newList[1], self.newList[2], self.newList[3])
            elif content.lower() == 'e':
                return self.render.reply_news(fromUser, toUser, int(time.time()), self.eatList[0], self.eatList[1], self.eatList[2], self.eatList[3])
            elif content.lower() == 'a':
                return self.render.reply_news(fromUser, toUser, int(time.time()), self.artList[0], self.artList[1], self.artList[2], self.artList[3])
            elif self.mc.get(fromUser) == 'fanyi':
                if type(content).__name__ == "unicode":
                    content = content.encode('utf-8')
                Nword = self.youdao(content)
                return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)
            elif self.mc.get(fromUser) == 'exit':
                return self.render.reply_text(fromUser,toUser,int(time.time()),self.replayText[1])



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
