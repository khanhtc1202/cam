#!/bin/bash

INTERPRETER=python2
HOST=0.0.0.0
PORT=8888
MODE=server

WORK_DIR="`pwd`/"

function usage() {
  cat << EOS
usage $0 [-m server|client] [-h 0.0.0.0|127.0.0.1] [-p 8888]
EOS
  exit 1
}

function start_server() {
  echo START CAM SERVER ON ${HOST}:${PORT}
  cd ${WORK_DIR}/server
  ${INTERPRETER} main.py ${HOST} ${PORT}
}

function start_client() {
  echo START CAM CLIENT ON ${HOST}:${PORT}
  cd ${WORK_DIR}/client
  case $(uname -n) in
    "raspberrypi" ) ${INTERPRETER} client_pi.py ${HOST} ${PORT} ;;
    "*" ) ${INTERPRETER} client_cv.py ${HOST} ${PORT} ;;
  esac
}

while getopts h:p:sc OPT
do
  case $OPT in
    "s" ) MODE=server ;;
    "c" ) MODE=client ;;
    "h" ) HOST=${OPTARG} ;;
	"p" ) PORT=${OPTARG} ;;
    "*" ) usage ;;
  esac
done

# run command
case ${MODE} in
  "server" ) start_server ;;
  "client" ) start_client ;;
esac
