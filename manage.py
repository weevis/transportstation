import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

from models import History, WorkQueue, NZBFile
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
