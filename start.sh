docker-compose build
docker-compose up

docker-compose run web python run.py db migrate
docker-compose run web python run.py db upgrade
