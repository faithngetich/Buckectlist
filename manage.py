import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db

app = create_app(os.getenv('ECOM_ENV') or 'dev')
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db(name):
    """Creates database with tables"""
    os.system('createdb {}'.format(name))
    db.create_all()
    print("{} has been successfully created.".format(name))

@manager.command
def drop_db(name):
    """Deletes a database"""
    os.system('dropdb {}'.format(name))
    db.drop_all()
    # db.session.commit()
    print("{} has been deleted.".format(name))

if __name__ == '__main__':
    manager.run()