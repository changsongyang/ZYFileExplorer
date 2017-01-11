#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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
    favorid = Column(Integer)


class Direcord(Base):
    __tablename__ = 'direcord'
    dirmd5 = Column(String(32), primary_key=True)
    dirname = Column(String(255), nullable=False)
    total = Column(Integer, nullable=False)
    favorcount = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
# init_db()
Session = sessionmaker(bind=engine)
session = Session()


def query_favor(imgmd5):
    ret = session.query(Favor).filter_by(imgmd5=imgmd5).first()
    session.close()
    if ret:
        return ret.favorid


def query_dir(dirmd5):
    ret = session.query(Direcord).filter_by(dirmd5=dirmd5).first()
    session.close()
    if ret:
        return [ret.total, ret.favorcount, ret.status]


def query_favor_dir(imgdirmd5):
    ret = session.query(Favor).filter_by(imgdirmd5=imgdirmd5, favorid=1).all()
    session.close()

    if ret:
        return len(ret)
    else:
        return 0


def write_favor(imgmd5, imgname, imgdir, imgdirmd5, favorid):
    ret = session.query(Favor).filter_by(imgmd5=imgmd5).first()

    if not ret:
        obj = Favor(imgmd5=imgmd5, imgname=imgname, imgdir=imgdir, imgdirmd5=imgdirmd5, favorid=favorid)
        session.add(obj)
    else:
        session.query(Favor).filter(Favor.imgmd5 == imgmd5).update({"favorid": favorid})

    session.commit()


def write_dir(dirmd5, dirname, total, favorcount, status):
    ret = session.query(Direcord).filter_by(dirmd5=dirmd5).first()

    if not ret:
        obj = Direcord(dirmd5=dirmd5, dirname=dirname, total=total, favorcount=favorcount, status=status)
        session.add(obj)
    else:
        session.query(Direcord).filter(Direcord.dirmd5 == dirmd5).update(
            {"total": total, "favorcount": favorcount, "status": status})

    session.commit()


def update_dir(dirmd5, status):
    session.query(Direcord).filter(Direcord.dirmd5 == dirmd5).update(
        {"status": status})

    session.commit()
