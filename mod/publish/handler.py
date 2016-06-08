# -*- coding: utf-8 -*-
# @Date    : 2016/6/3  10:54
# @Author  : 490949611@qq.com

import tornado.web
from ..db.material import Material
import json
from config import *

class PublishHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def get(self):
		if self.current_user != ADMIN_STUDENTNUM:
			self.write("您没有权限访问本页面")
		else:
			material = self.db.query(Material).all()
			self.render('publish.html',data = material)

	def post(self):
		retjson={
			'code':200,
			'content':''
		}

		title = self.get_argument('title',default=None)
		url = self.get_argument('url',default=None)
		author = self.get_argument('author',default=None)
		id = self.get_argument('id',default=None)
		delete = self.get_argument('dlt',default=0)


		print "delete",delete,"id",id
		if int(delete) == 1:
			try:
				print 'try to remove'
				material = self.db.query(Material).filter(Material.id == id).one()
				self.db.delete(material)
				self.db.commit()
				retjson['content'] = u'删除成功！'
			except Exception,e:
				retjson['content'] = u'删除失败,请重新尝试'
		else:
			try:
				print 'enter'
				material = Material(title = title,url = url,author = author)
				self.db.add(material)
				self.db.commit()
				retjson['content'] = u'发布成功！'
			except Exception,e:
				retjson['code'] = 400
				retjson['content'] = u'发布失败'
		self.write(json.dumps(retjson))
		self.finish()

	def remove(self,id,retjson):
		try:
			print 'try to remove'
			material = self.db.query(Material).filter(Material.id == id).one()
			self.db.delete(material)
			self.db.commit()
			retjson['content'] = u'删除成功！'
		except Exception,e:
			retjson['content'] = u'删除失败,请重新尝试'

