# -*- coding: utf-8 -*-
# @Date    : 2016/8/25  14:40
# @Author  : 490949611@qq.com

import tornado.web

class HostHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('firstpage.html')