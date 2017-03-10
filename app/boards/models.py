from datetime import datetime, timedelta

from app import db
from app.utils.misc import make_code


#def expiration_date():
#    return datetime.now() + timedelta(days=1)


class AppBoard(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String(255))
    order = db.Column(db.Integer(), unique=True)
    modified = db.Column(db.String(255), unique=True)

    def __init__(self, user, name, order):
        self.user = user
        self.name = name
        self.order = order
        self.modified = datetime.now()


    #def deactivate(self):
        #self.active = False
