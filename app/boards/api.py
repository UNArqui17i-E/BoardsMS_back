from datetime import datetime

from flask import g
from flask.ext import restful
from flask import request
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.exc import IntegrityError


from app.boards.mixins import SignupLoginMixin
from app.boards.models import AppBoard

from app.utils.auth import auth_required, admin_required, generate_token
from app.utils.errors import EMAIL_IN_USE, CODE_NOT_VALID, BAD_CREDENTIALS, SERVER_ERROR, NO_CONTENT

from app import db, bcrypt


board_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'order': fields.Integer,
    'user': fields.Integer
}


class BoardAPI(SignupLoginMixin, restful.Resource):

    #@auth_required
    @marshal_with(board_fields)
    def get(self):
        ide = request.args.get('id')
        ide = int(ide)
        board = db.session.query(AppBoard).filter(AppBoard.id==ide).first()
        if board is not None:
            return board
        else:
            return NO_CONTENT

    def post(self):
        args = self.req_parser.parse_args()
        length = db.session.query(AppBoard).all()
        cont = len(length) + 1
        board = AppBoard(name=args['name'], user=args['user'], order=cont)
        db.session.add(board)

        try:
            db.session.commit()
        except IntegrityError:
            return SERVER_ERROR
        return {
            'id': board.id
        }, 201

    def delete(self):
        ide = request.args.get('id')
        ide = int(ide)
        board = db.session.query(AppBoard).filter(AppBoard.id==ide).first()
        if board is not None:
            db.session.delete(board)

            try:
                db.session.commit()
            except IntegrityError:
                return NO_CONTENT
        else:
            return NO_CONTENT

    def put(self):
        args = self.req_parser.parse_args()
        ide = int(args['id'])
        board = db.session.query(AppBoard).filter(AppBoard.id==ide).first()


        if board is not None:
            board.name = args['name']

            try:
                db.session.commit()
            except IntegrityError:
                return SERVER_ERROR
        else:
            return NO_CONTENT





class BoardsByUserAPI(SignupLoginMixin, restful.Resource):

    #@auth_required
    @marshal_with(board_fields)
    def get(self):
        ide = request.args.get('id')
        ide = int(ide)
        #bo = db.session.query(AppBoard).filter(AppBoard.id==ide).first()
        #return bo
        boards = db.session.query(AppBoard).filter(AppBoard.user==ide).all()
        return boards

class Board(SignupLoginMixin, restful.Resource):

    #@auth_required
    @marshal_with(board_fields)
    def get(self):
        boards = db.session.query(AppBoard).all()
        return boards
