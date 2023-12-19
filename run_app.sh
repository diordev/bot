docker run --name db -e POSTGRES_PASSWORD=1 -e POSTGRES_USER=postgres -e POSTGRES_DB=bot -p 5432:5432 -d --network=webnet  --restart=always  postgres
docker build -t django_app ~/bot/waiter_admin/ 
docker run --name admin  -p 80:8000 -d --network=webnet  --restart=always  django_app
docker build -t bot_app ~/bot/waiter_bot/
docker run --name bot -d --network=webnet  --restart=always  bot_app
