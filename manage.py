#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from movie import create_app
from movie.models import db, User, Userlog, Tag, Movie, Preview, Comment, Moviecol, Auth, Role, Admin, Adminlog, Oplog


env = os.environ.get('BLOG_ENV', 'dev')

app = create_app('settings.%sConfig' % env.capitalize())

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Tag=Tag,
                Movie=Movie,
                Preview=Preview,
                Comment=Comment,
                Moviecol=Moviecol,
                Auth=Auth,
                Admin=Admin,
                Adminlog=Adminlog,
                Oplog=Oplog)

if __name__ == '__main__':
    manager.run()
