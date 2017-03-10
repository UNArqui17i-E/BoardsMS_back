from datetime import datetime

from flask import g
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.exc import IntegrityError


from app.boards.mixins import SignupLoginMixin
from app.boards.models import AppBoard, PasswordReset

from app.utils.auth import auth_required, admin_required, generate_token
from app.utils.errors import EMAIL_IN_USE, CODE_NOT_VALID, BAD_CREDENTIALS, SERVER_ERROR

from app import db, bcrypt


board_fields = {
    'name': fields.String,
    'order': fields.Integer,
    'user': fields.Integer
}


class BoardAPI(SignupLoginMixin, restful.Resource):

    #@auth_required
    @marshal_with(board_fields)
    def get(self):
        return "si"

    def post(self):
        args = self.req_parser.parse_args()

        board = AppBoard(name=args['name'], order=args['order'], user=args['user'])
        db.session.add(board)

        try:
            db.session.commit()
        except IntegrityError:
            return SERVER_ERROR

        return {
            'id': board.id
        }, 201


class AuthenticationAPI(SignupLoginMixin, restful.Resource):

    def post(self):
        args = self.req_parser.parse_args()

        user = db.session.query(AppUser).filter(AppUser.email==args['email']).first()
        if user and bcrypt.check_password_hash(user.password, args['password']):

            return {
                'id': user.id,
                'token': generate_token(user)
            }

        return BAD_CREDENTIALS


class PasswordResetRequestAPI(restful.Resource):

    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('email', type=str, required=True)
        args = req_parser.parse_args()

        user = db.session.query(AppUser).filter(AppUser.email==args['email']).first()
        if user:
            password_reset = PasswordReset(user=user)
            db.session.add(password_reset)
            db.session.commit()
            # TODO: Send the email using any preferred method

        return {}, 201


class PasswordResetConfirmAPI(restful.Resource):

    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('code', type=str, required=True)
        req_parser.add_argument('password', type=str, required=True)
        args = req_parser.parse_args()

        password_reset = db.session.query(PasswordReset
                            ).filter(PasswordReset.code==args['code']
                            ).filter(PasswordReset.date>datetime.now()).first()

        if not password_reset:
            return CODE_NOT_VALID

        password_reset.user.set_password(args['password'])
        db.session.delete(password_reset)
        db.session.commit()

        return {}, 200



class AdminOnlyAPI(restful.Resource):

    @admin_required
    def get(self):
        return {}, 200
