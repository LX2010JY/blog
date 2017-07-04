import os
from app import create_app,db
from app.models import User,Role
from app.model.blog import Blog,Blog_Type
from flask_script import Manager,Shell
from flask_migrate import MigrateCommand,Migrate

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Blog=Blog,Blog_Type=Blog_Type)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

# @manager.command
# def test():
#     '''
#         运行单元测试
#     :return:
#     '''
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8080)
    manager.run()
