# -*- coding:utf-8 -*-
# 模拟登陆豆瓣
import http.cookiejar as cookielib
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from PIL import Image

import tesserocr

class DoubanLogin():
  def __init__(self):
    self.session = requests.Session()
    self.session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
    self.url = 'https://accounts.douban.com/login'
    self.redirurl = 'https://book.douban.com/mine'
    self.email = '******'
    self.password = '******'
    # 构造post数据
    self.data = {
      'redir': self.redirurl,
      'form_email': self.email,
      'form_password': self.password,
      'login': '登录'
    }
    self.headers = {
      'User-Agent': 'Mozilla/5.0 '
      '(Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/55.0.2883.87 Safari/537.36'
    }

  def get_index(self):
    # 根据本地cookies登录
    try:
      self.session.cookies.load(ignore_discard=True)
    except Exception as e:
      print("cookie未能加载, 原因: ", e)
    response = self.session.get(self.redirurl, headers=self.headers)
    with open("index.html", 'wb') as f:
      f.write(response.text)
    print("ok")

  def process_captcha(self, page, captcha):
    # 处理验证码
    # 获得验证码图片地址
    captcha_url = captcha['src']
    # 利用正则表达式获得验证码ID
    pattern = re.compile('<input type="hidden" name="captcha-id" value="(.*?)"/')
    captcha_id = re.search(pattern, page.text).group(1)
    # 将验证码图片保存到本地
    urllib.request.urlretrieve(captcha_url, "captcha.png")
    captcha = input('please input the captcha:')
    self.data['captcha-solution'] = captcha
    self.data['captcha-id'] = captcha_id

  def is_login(self):
    main_url = "https://book.douban.com/mine"
    response = self.session.get(main_url, headers=self.headers, allow_redirects=False)
    print(response.text)
    if response.status_code != 200:
      return False
    else:
      return True

  def login(self):
    page = self.session.post(self.url, headers=self.headers)
    soup = BeautifulSoup(page.text, "html.parser")
    captcha = soup.find('img', id='captcha_image')
    if captcha is not None:
      self.process_captcha(page, captcha)
      afterLogin_page = self.session.post(self.url, data=self.data, headers=self.headers)
    else:
      afterLogin_page = self.session.post(self.url, data=self.data, headers=self.headers)
    # print(self.session.cookies)
    self.session.cookies.save(ignore_discard=True, ignore_expires=True)
    print(afterLogin_page.text)
    soup = BeautifulSoup(afterLogin_page.text, "html.parser")
    result = soup.findAll('div', attrs={'class': 'title'})
    for item in result:
      print(item.find('a').get_text())

douban = DoubanLogin()
douban.login()
douban.get_index()
print(douban.is_login())
