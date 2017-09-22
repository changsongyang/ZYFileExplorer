#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings

mysqldict = settings.mysqlconfig()

engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
    mysqldict['User'], mysqldict['Pwd'], mysqldict['DBHost'], mysqldict['DBPort'], mysqldict['Database']),
                       max_overflow=5)

Base = declarative_base()


class Favor(Base):
    __tablename__ = 'favor'
    imgmd5 = Column(String(32), primary_key=True)
    imgname = Column(String(255), nullable=False)
    imgdir = Column(String(255), nullable=False)
    imgdirmd5 = Column(String(32), nullable=False, index=True)


class Direcord(Base):
    __tablename__ = 'direcord'
    dirmd5 = Column(String(32), primary_key=True)
    dirname = Column(String(255), nullable=False)
    total = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)


class TagsToFavor(Base):
    __tablename__ = 'tagstofavor'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    favor_id = Column(String(32), ForeignKey('favor.imgmd5'))


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
# init_db()
Session = sessionmaker(bind=engine)
session = Session()


def query_alltag():
    alltag = session.query(Tags.id, Tags.name).all()
    return alltag


def query_tag(imgmd5):
    imgtag = session.query(Tags.name).join(TagsToFavor).filter(TagsToFavor.favor_id == imgmd5).all()
    str = '当前标签:'
    for i in imgtag:
        str += '{},'.format(i[0])

    session.close()
    return str


def query_dir(dirmd5):
    ret = session.query(Direcord).filter_by(dirmd5=dirmd5).first()
    session.close()
    if ret:
        return [ret.total, ret.status]


def write_tag(name):
    ret = session.query(Tags).filter_by(name=name).first()
    id = None
    if not ret:
        obj = Tags(name=name)
        session.add(obj)
        session.flush()  # 在commit提交前执行这几句就可以获取自增id，不用再次去数据库查询
        session.refresh(obj)
        id = obj.id
    session.commit()
    return id


def write_tag_favor(tagid, favorid):
    ret = session.query(TagsToFavor).filter_by(tag_id=tagid, favor_id=favorid).first()

    if not ret:
        obj = TagsToFavor(tag_id=tagid, favor_id=favorid)
        session.add(obj)
    session.commit()


def write_favor(imgmd5, imgname, imgdir, imgdirmd5):
    ret = session.query(Favor).filter_by(imgmd5=imgmd5).first()

    if not ret:
        obj = Favor(imgmd5=imgmd5, imgname=imgname, imgdir=imgdir, imgdirmd5=imgdirmd5)
        session.add(obj)

    session.commit()


def write_dir(dirmd5, dirname, total, status):
    ret = session.query(Direcord).filter_by(dirmd5=dirmd5).first()

    if not ret:
        obj = Direcord(dirmd5=dirmd5, dirname=dirname, total=total, status=status)
        session.add(obj)
    else:
        session.query(Direcord).filter(Direcord.dirmd5 == dirmd5).update(
            {"total": total, "status": status})

    session.commit()


def update_dir(dirmd5, status):
    session.query(Direcord).filter(Direcord.dirmd5 == dirmd5).update(
        {"status": status})

    session.commit()
