docker-compose build
docker-compose up
docker-compose run --rm web python run.py db migrate
docker-compose run --rm web python run.py db upgrade
