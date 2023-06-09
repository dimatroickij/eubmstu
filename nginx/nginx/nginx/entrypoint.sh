#!/bin/bash

array=$(echo $VIRTUAL_HOST | tr "," "\n")

for element in $array
do
 cat default.conf > /vhost/$element
done