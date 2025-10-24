#!/bin/bash

array=$(echo $DJANGO_ALLOWED_HOSTS | tr " " "\n")

for element in $array
do
 cat default.conf > /vhost/$element
done