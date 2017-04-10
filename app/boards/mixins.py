from flask.ext.restful import reqparse


class SignupLoginMixin(object):

    req_parser = reqparse.RequestParser()
    # req_parser.add_argument('id', type=int, required=False)
    req_parser.add_argument('name', type=str, required=True)
    req_parser.add_argument('user', type=int, required=True)
