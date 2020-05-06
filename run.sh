docker stop ipblock
docker rm ipblock
nohup docker run --name ipblock -p 5002:5002 ipblock &
