# itmo-containers

docker rmi -f bad_docker && docker build -f dockerfile.bad -t bad_docker . && docker run -p 80:80 -it bad_docker

docker rmi -f good_docker && docker build -f dockerfile.good -t good_docker . && docker run -p 80:80 -it good_docker