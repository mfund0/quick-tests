FROM python:2-alpine

COPY docker-images/diamond/requirements.txt ./
RUN apk update \
 && apk upgrade \
 && apk add --no-cache --virtual .build-deps build-base linux-headers git \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps \
 && rm -rf /var/cache/apk/*
 COPY docker-images/diamond/diamond.conf /etc/diamond/diamond.conf
 COPY docker-images/diamond/entrypoint.sh /bin/entrypoint.sh

 ENTRYPOINT ["/bin/entrypoint.sh"]