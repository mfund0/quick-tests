#!/bin/sh

sed -i \
  -e "s/<--HANDLERS-->/${HANDLERS}/g" \
  -e "s/<--PREFIX-->/${PREFIX}/g" \
  /etc/diamond/diamond.conf
diamond -f -l --skip-pidfile $@