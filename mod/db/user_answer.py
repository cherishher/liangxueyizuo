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
    username = Column(String(128), nullable=False)
    goal = Column(Integer,nullable=False)
    chance = Column(Integer,default=2)
    degree = Column(Integer,nullable=False)
    answer = Column(String(128), nullable=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)