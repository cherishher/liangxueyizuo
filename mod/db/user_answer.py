# -*- coding: utf-8 -*-
# @Date    : 2016/5/24  19:56
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Answer(Base):
    __tablename__ = 'answer_situation'
    id = Column(Integer, primary_key=True)
    username = Column(String(4096), nullable=False)
    goal = Column(Integer,nullable=False)
    time = Column(String(64), nullable=False)
    type = Column(Integer,nullable=False)

if __name__ == '__main__':
	Base.metadata.create_all(engine)