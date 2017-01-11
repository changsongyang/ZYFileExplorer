#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from views import index

settings = {
    'template_path': 'templates',
    'static_path': 'statics',
}

application = tornado.web.Application([
    (r"/photo(?P<url>/.*)", index.PhotoHandler),
    (r"/favor", index.FavorHandler),
    (r"/count", index.CountHandler),
    (r"/del", index.DelHandler),
    (r"/.*", index.IndexHandler),
], **settings)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()