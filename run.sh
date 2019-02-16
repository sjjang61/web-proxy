#!/bin/sh
APP_NAME=web-proxy
APP_MAIN=serverMain.py
APP_HOME=/home/ec2-user/deploy/web-proxy/{APP_NAME}

function stop(){
	echo 'stop WEB_PARSER_TOOL...'
	
	PID=$(ps -ef | grep serverMain.py | grep -v "grep" | awk '{print $2}')
  echo "- pid : ${PID}"
    
	if [[ ! -z $PID ]]; then
		echo "- kill process"
		kill -9 ${PID}
	else
		echo "- no process"
	fi                  
}

function start(){
	echo 'start ${APP_NAME}...'
	nohub python3 ${APP_HOME}/${APP_MAIN} &
}

function restart(){
	echo 'restart ${APP_NAME}...'
	stop
	start
}

OPTION=$1

case $OPTION in
                "start")
                start
                ;;

                "stop")
                stop
                ;;
                
                "restart")
                restart
                ;;

        *)
            echo "[usage] : $0 start|stop|reload|restart"
        ;;
esac
