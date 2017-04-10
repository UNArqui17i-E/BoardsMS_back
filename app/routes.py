from app import rest_api

from boards import api as board_api


rest_api.add_resource(board_api.BoardAPI, '/api/v1/board')
rest_api.add_resource(board_api.BoardsByUserAPI, '/api/v1/boardsbyuser')
rest_api.add_resource(board_api.Boards, '/api/v1/boards')
