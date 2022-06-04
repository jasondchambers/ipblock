docker build --tag ipblock .
docker stop ipblock
docker rm ipblock
nohup docker run --restart unless-stopped --name ipblock -p 5002:5002 ipblock &
