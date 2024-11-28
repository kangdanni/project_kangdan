docker-compose build
docker-compose run --rm app django-admin startproject app .
docker-compose up
docker exec -it django_container /bin/bash


docker exec -it mysql_db /bin/bash
mysql -uroot --port 3306 < ./docker-entrypoint-initdb.d/initial_data.sql