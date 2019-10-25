#!/bin/bash
#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update &&


mkdir /usr/mirror &&

PARAM_FILE=/usr/monitor/mirror.cfg
echo "tmt" > $PARAM_FILE
echo "tmf=$1" >> $PARAM_FILE
echo "region=$2" >> $PARAM_FILE
