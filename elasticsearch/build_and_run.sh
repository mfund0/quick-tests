docker build --tag=elasticsearch .
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -ti -v /usr/share/elasticsearch/data elasticsearch
#-e "network.bind_host=0.0.0.0" -e "http.host=0.0.0.0"
#docker.elastic.co/elasticsearch/elasticsearch:7.8.0