docker build -t filebeat .
docker run --net=host -p 8081:8081 filebeat