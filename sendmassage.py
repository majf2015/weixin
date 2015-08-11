# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SendMassage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://mp.weixin.qq.com"
        self.account = '1021008546@qq.com'
        self.pwd = '587921MJF'
    
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("account").clear()
        driver.find_element_by_id("account").send_keys(self.account)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(self.pwd)
        driver.find_element_by_id("loginBt").click()
        driver.find_element_by_link_text(u"群发功能").click()
        driver.find_element_by_css_selector("span.msg_tab_title").click()
        driver.find_element_by_css_selector("i.icon36_common.add_gray").click()
        driver.find_element_by_css_selector("div.appmsg.multi > div.appmsg_mask").click()
        driver.find_element_by_css_selector("button.js_btn").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()

    
