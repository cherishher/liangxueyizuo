#!/usr/bin/env python
#coding:utf-8
# @Date    : 2015-12-8 12:46:36
# @Author  : 490949611@qq.com

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PWD = 'XXXXX'
DB_NAME = 'partymem'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                       (DB_USER, DB_PWD, DB_HOST, DB_NAME), echo=False,pool_size=500, pool_recycle=100)