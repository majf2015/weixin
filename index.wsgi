# coding: UTF-8
import os
import sys

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'beautifulsoup'))
import sae
import web
from weixinInterface import WeixinInterface
from browserhandler import BrowserHandler
from menu import CreatMenu
from sendmessage import SendMessage


urls = (
    '/weixin', 'WeixinInterface',
    '/web', 'BrowserHandler'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()


class MyApp:
    def __init__(self, a):
        self.a_ = a
        self.StartTimer()

    def __call__(self, env, resp):
        return self.a_(env, resp)

    def StartTimer(self):
        menu = CreatMenu()
        menu.PostMenu()
        send = SendMessage()
        send.PostMessage()
        print "hellow MyApp ffffffffffffffffffffffff"


my_app = MyApp(app)
application = sae.create_wsgi_app(my_app)
