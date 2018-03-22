#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask_script import Manager, Shell, Server
from movie import app
from settings import DevConfig

app.config.from_object(DevConfig)

manager = Manager(app)
manager.add_command('server', Server())

@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == '__main__':
    manager.run()
