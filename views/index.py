#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from views import photo
from views import filecheck
from models import zyimg
import urllib.request  # 中文url传到程序变为%E9%97%B2%E9%B1%BC这种格式，需要解码,使用urllib.request.unquote()
import os
import settings
import json


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # 对中文uri解码
        URI = urllib.request.unquote(self.request.uri)[1:]

        # 获取上一级uri
        previous = self.request.uri.rsplit('/', 1)[0]
        # 当已经在首页，上一页仍然是首页
        if not previous:
            previous = '/'

        result = photo.dircontent(URI)

        if isinstance(result, dict):
            html_list = []
            html_head = '<h1><span class="label label-primary"><i class="fa fa-folder-open" aria-hidden="true"></i>当前目录内容</span><span class="badge">%s</span></h1><nav><ul class="pager"><li><a href="/">首页</a></li><li><a href="%s">返回上一层</a></li></ul></nav>' % (
                self.request.uri, previous)
            html_list.append(html_head)

            if len(result['dir']):
                html_list.append(
                    '<h2><span class="label label-success"><i class="fa fa-folder-open" aria-hidden="true"></i>子目录</span></h2><div class="container-fluid">')
                for i in result['dir']:
                    dirname = '%s/%s' % (URI, i) if URI else  '%s' % i
                    dirmd5 = filecheck.md5str(dirname)
                    dirinfo = zyimg.query_dir(dirmd5)
                    if not dirinfo:
                        dirinfo = ['null', 'null', 'null']

                    data_orign = '/%s/%s' % (URI, i) if URI else '/%s' % i
                    if dirinfo[2] == 0:
                        css_status = 'disabled'
                        href = 'javascript:void(0)'
                        title = '激活'
                    else:
                        css_status = ''
                        href = data_orign
                        title = '删除'

                    html_dir = '<div class="row"><div class="col-md-11"><a class="list-group-item %s" href="%s"  data-orign="%s"><span class="glyphicon glyphicon-folder-open"> </span>%s<span class="badge love">喜欢：%s</span><span class="badge total">总数：%s</span></a></div><div class="btn-group col-md-1"><button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown">操作 <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a class="count" href="javascript:void(0)">统计</a></li><li><a class="del" href="javascript:void(0)">%s</a></li></ul></div></div>' % (
                        css_status, href, data_orign, i, dirinfo[1], dirinfo[0], title)
                    html_list.append(html_dir)

                html_list.append('</div>')

            if len(result['img']):
                html_img1 = '<h2><span class="label label-info"><i class="fa fa-picture-o" aria-hidden="true"></i><a href="/photo/%s">图片</a></span></h2>' % URI
                html_list.append(html_img1)
                for i in result['img']:
                    html_img2 = '<a class="list-group-item" href="/static/mountfile/%s/%s"><i class="fa fa-picture-o" aria-hidden="true"></i>%s</a>' % (
                        URI, i, i)
                    html_list.append(html_img2)

            if len(result['oth']):
                html_list.append('<h2><span class="label label-warning">其他</span></h2>')
                for i in result['oth']:
                    html_oth = '<li class="list-group-item">%s</li>' % i
                    html_list.append(html_oth)

            self.render('content.html', htmlcontent=''.join(html_list))
        else:
            self.write('页面不存在')


class PhotoHandler(tornado.web.RequestHandler):
    def get(self, url):
        URL = urllib.request.unquote(url)[1:]

        result = photo.dircontent(URL)
        root = settings.root()
        if isinstance(result, dict):
            html_list = []
            for i in result['img']:
                if URL:
                    imgurl = '/static/mountfile/%s/%s' % (URL, i)
                else:
                    imgurl = '/static/mountfile/%s' % i
                imgpath = imgurl.replace('/static/mountfile/', '', 1)
                imgfile = os.path.normpath(os.path.join(root, imgpath))
                imgmd5 = filecheck.md5file(imgfile)
                favorid = zyimg.query_favor(imgmd5)

                # if favorid == 1:
                #     favorurl = '<span style="color:red"><i class="fa fa-heart fa-3x" aria-hidden="true"></i></span>'
                # else:
                #     favorurl = '<span style="color:red"><i class="fa fa-3x fa-heart-o" aria-hidden="true"></i></span>'
                #
                # html_content = '<div class="img-list"><div style="position: relative"><div class="item"><img class="lazy" data-original="%s" /></div><div style="position:absolute;bottom: 0;right: 0;">%s</div></div><div style="height: 20px"></div>' % (
                #     imgurl, favorurl)

                html_content = '<li><img src="{}" /></li>'.format(imgurl)

                html_list.append(html_content)

            self.render('photo2.html', htmlcontent=''.join(html_list))


class FavorHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        imgurl = self.get_argument('imgurl')
        favorid = self.get_argument('favorid')
        imgpath = imgurl.replace('/static/mountfile/', '', 1)
        root = settings.root()
        imgfile = os.path.normpath(os.path.join(root, imgpath))
        imgmd5 = filecheck.md5file(imgfile)
        try:
            imgname = imgpath.rsplit('/', 1)[1]
            imgdir = imgpath.rsplit('/', 1)[0]
        except IndexError as e:
            imgname = imgpath
            imgdir = '/'
        imgdirmd5 = filecheck.md5str(imgdir)

        zyimg.write_favor(imgmd5, imgname, imgdir, imgdirmd5, favorid)


class CountHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        dirurl = self.get_argument('url')
        dirname = dirurl.replace('/', '', 1)
        dirmd5 = filecheck.md5str(dirname)
        root = settings.root()
        dirpath = os.path.normpath(os.path.join(root, dirname))
        total = len([x for x in os.listdir(dirpath)])
        favorcount = zyimg.query_favor_dir(dirmd5)
        dirinfo = [total, favorcount, 1]
        zyimg.write_dir(dirmd5, dirname, total, favorcount, 1)
        self.write(json.dumps(dirinfo))


class DelHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        dirurl = self.get_argument('url')
        status = self.get_argument('status')
        dirname = dirurl.replace('/', '', 1)
        dirmd5 = filecheck.md5str(dirname)
        zyimg.update_dir(dirmd5, status)
