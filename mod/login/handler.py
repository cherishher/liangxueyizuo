# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com

from mod.db.member import Member
import tornado.web
import datetime
import json,urllib

class LoginHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get(self):
		self.write("hello guys!")

	def post(self):
		flag = True
		studentnum = self.get_argument('studentnum',default=None)
		password = self.get_argument('password',default=None)

		data = self.db.query(Member).filter(Member.studentnum == studentnum).one()
		print data.password
		if data.password == password:
			self.write('login success')
		else:
			self.write('login failed')

