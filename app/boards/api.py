from datetime import datetime

from flask import g
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.exc import IntegrityError


from app.boards.models import AppBoard

from app.utils.auth import auth_required, admin_required, generate_token
from app.utils.errors import EMAIL_IN_USE, CODE_NOT_VALID, BAD_CREDENTIALS, SERVER_ERROR

from app import db, bcrypt


boards_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'order': fields.Integer,
    'user': fields.Integer,
    'modified': fields.String
}


class BoardAPI(restful.Resource):

    #@auth_required
    @marshal_with(boards_fields)
    def get(self):
        args = self.req_parser.parse_args()
        users=args['user']
        return AppBoard.query.filter_by(user=user)


    def post(self):
        args = self.req_parser.parse_args()

        board = AppBoard( name=args['name'], order=args['order'], user=args['user'])
        #db.session.add(user)
        db.session.add(board)

        try:
            db.session.commit()
        except IntegrityError:
            return SERVER_ERROR

        return {
            'id': board.id,
        }, 201




class AdminOnlyAPI(restful.Resource):

    @admin_required
    def get(self):
        return {}, 200
