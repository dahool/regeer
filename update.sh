#!/bin/bash
BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR"; pwd)`
cd $BASEDIR
echo "Fetch updates ..."
git pull
sh appupdate.sh
cd -
