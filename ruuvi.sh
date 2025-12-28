#!/bin/bash

# Path to the application and PID file
# APP_COMMAND="/path/to/application/start_command"
APP_COMMAND="uvicorn ruuvi_api:app --host 0.0.0.0 --port  --no-access-log"
PID_FILE="ruuvi_api.pid"
LOG_FILE="ruuvi_api.log"
BASLE_DIR="ruuvi/"

set_env() {
  cd $BASLE_DIR
  if [ -z "$VIRTUAL_ENV" ]; then
    echo "No virtual environment active"
    if [ -f "venv/bin/activate" ]; then
      . venv/bin/activate
    else
      python3 -m venv venv
      . venv/bin/activate
    fi
  fi
  # lets take a look
  if [ ! -z "$VIRTUAL_ENV" ]; then  # virtual env is active
    echo "Virtual environment active: $VIRTUAL_ENV"
    pip install -r requirements.txt
  else
    echo "Failed to activate virtual environment for ruuvi api gw." | mailx -s "Error: Ruuvi_api.py not started"  ilkka.mattila@oivoi.org
    exit 1
  fi

}

start_app() {
    # Check if the application is already running
    cd $BASLE_DIR
    set_env
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "Application is already running."
    else
        echo "Starting application..."
        # Start the application in the background and save its PID
	$APP_COMMAND > $LOG_FILE 2>&1 &
        echo $! > "$PID_FILE"
        echo "Application started with PID $(cat $PID_FILE)."
    fi
}

stop_app() {
    # Check if the application is running
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "Stopping application..."
        kill -9 $(cat "$PID_FILE") # Send a kill signal to the application
        rm -f "$PID_FILE"           # Remove the PID file
        echo "Application stopped."
    else
        echo "Application is not running."
    fi
}

status_app() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "Application is running with PID $(cat "$PID_FILE")."
    else
        echo "Application is not running."
	start_app
    fi
}

case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    status)
        status_app
        ;;
    restart)
        stop_app
        start_app
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit 0
