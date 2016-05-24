# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from mod.db.member import Member
import tornado.web
import datetime
import json,urllib
from tornado.httpclient import HTTPRequest,HTTPClient

class RegisterHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get(self):
		self.render('register.html')

	def post(self):
		flag = True
		type = self.get_argument("type",default=None)
		studentnum = self.get_argument("studentnum",default=None)
		name = self.get_argument("name",default=None).encode('utf-8')
		password = self.get_argument("password",default=None)
		repepassword = self.get_argument("repepassword",default=None)
		phonenum = self.get_argument('phonenum',default=None)
		college = self.get_argument("college",default=None).encode('utf-8')
		branch = self.get_argument("branch",default=None).encode('utf-8')
		if not (studentnum or name or password or phonenum or college or branch):
			self.write("缺少必要信息！请重新填写")
			flag = False
		elif len(phonenum)!= 11:
			self.write("手机号不符合要求，请重新填写")
			flag = False
		elif repepassword != password:
			self.write("两次密码输入不一致，请重新填写")
			flag = False
		try:
			data = self.db.query(Member).filter(Member.studentnum == studentnum).one()
			if data:
				self.write("该学号已被注册，请重新填写")
				flag = False
		except Exception,e:
			print str(e)
		# typedef = {
		# 	0:nothing(self,studentnum),
		# 	1:nothing(self,name),
		# 	2:nothing(self,password),
		# 	3:repassword(self,password,repepassword),
		# 	4:nothing(self,phonenum),
		# 	5:nothing(self,college),
		# 	6:nothing(self,branch)
		# }
		if flag:
			try:
				new_user = Member(studentnum= studentnum,password=password,name=name,phonenum=phonenum,college=college,branch=branch)
				self.db.add(new_user)
				self.db.commit()
				print 'new_user added'
			except Exception,e:
				print(e)
				self.write("注册失败，请重新填写")

	def check_user(self,num):
		data = self.db.query(Member).filter(Member.studentnum == num).one()
		if data:
			return False
		else:
			return True

	def nothing(self,param):
		if not param:
			self.write("lack of param")
			return False
		return True

	def repassword(self,param1,param2):
		if param1!=param2:
			self.write('repassword wrong')
			return False
		return True

