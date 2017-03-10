from app import rest_api

from boards import api as board_api


rest_api.add_resource(board_api.BoardAPI, '/api/v1/board')
