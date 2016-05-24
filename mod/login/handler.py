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
		self.render('login.html')

	def post(self):
		try:
			flag = True
			studentnum = self.get_argument('studentnum',default=None)
			password = self.get_argument('password',default=None)

			data = self.db.query(Member).filter(Member.studentnum == studentnum).one()
			print data.password
			if data.password == password:
				self.write('登录成功！')
			else:
				self.write('密码错误请重新输入密码')
		except Exception,e:
			self.write("该用户尚未注册，请注册后再登录")

