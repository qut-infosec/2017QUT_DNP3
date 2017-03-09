#!/bin/bash
_DATA_SET=$(echo "$1" | cut -d "/" -f4)
_ATTACK=$(echo "$1" | cut -d "/" -f3)
_DATA_TYPE=$(echo "$1" | cut -d "/" -f5)
filename=$_DATA_TYPE"."$_ATTACK"."$_DATA_SET
#echo $1
echo $filename
cp "$1" ~/Datasets/graphs/"$filename".ps
