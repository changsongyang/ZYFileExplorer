#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from views import index
import os

# 使用这种配置方式，在其他目录运行run.py也不会影响找不到templates和statics目录
template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "statics")
settings = {
    'template_path': template_path,
    'static_path': static_path,
}

application = tornado.web.Application([
    (r"/photo(?P<url>/.*)", index.PhotoHandler),
    (r"/tagquery", index.TagQueryHandler),
    (r"/tagadd", index.TagAddHandler),
    (r"/count", index.CountHandler),
    (r"/del", index.DelHandler),
    (r"/.*", index.IndexHandler),
], **settings)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
