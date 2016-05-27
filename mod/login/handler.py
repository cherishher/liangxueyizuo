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
		#验证用户身份
		try:
			retjson={
					'code':200,
					'text':"登录成功"
				}
			flag = True
			studentnum = self.get_argument('studentnum',default=None)
			password = self.get_argument('password',default=None)

			data = self.db.query(Member).filter(Member.studentnum == studentnum).one()
			if data.password == password:
				self.set_secure_cookie("user",studentnum)
			else:
				retjson['code'] = 400
				retjson['text'] = "密码错误，请重新登录"
		except Exception,e:
			print str(e)
			retjson['code'] = 401
			retjson['text'] = "该用户尚未注册，请注册后再登录"
		self.write(json.dumps(retjson))




