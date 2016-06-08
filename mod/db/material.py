# -*- coding: utf-8 -*-
# @Date    : 2016/6/3  10:32
# @Author  : 490949611@qq.com

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    title = Column(String(4096), nullable=False)
    url = Column(String(4096),nullable=False)
    author = Column(String(64), nullable=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)