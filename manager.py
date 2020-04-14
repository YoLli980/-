from  flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from project_traning import app
from exts import db
from  module import Student , Teacher,Class_known,Schedule,Proficiency,Curricula,Tmp_Curricula,Surper_root
manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()