# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest

class SendMassage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://mp.weixin.qq.com"
        self.account = 'your account'
        self.pwd = 'your password'
    
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("account").clear()
        driver.find_element_by_id("account").send_keys(self.account)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(self.pwd)
        driver.find_element_by_id("loginBt").click()


    
