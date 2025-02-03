#!/bin/bash

# Script o manage a systemd service - thermocouple_daemon.service.
# Note there is a copy (unused) of this service in HelperUtils

# Note the if statements do not work but the commands do
# Run this by ./manage_daemon enable/start/stop/restart/status

SERVICE_NAME="thermocouple_daemon.service"

# Function to check if the service file exists
check_service_file() {
    if [ ! -f "/etc/systemd/system/$SERVICE_NAME" ]; then
        echo "Error: Service file /etc/systemd/system/$SERVICE_NAME not found"
        return 1
    fi
    return 0
}

# Function to handle enable
enable_service() {
    check_service_file
    sudo systemctl enable "$SERVICE_NAME"
    if [ $? -eq 0]; then
        echo "Service $SERVICE_NAME enabled"
    else
        echo "Error enabling service $SERVICE_NAME"
    fi
}

# Function to handle start
start_service() {
    check_service_file
    sudo systemctl start "$SERVICE_NAME"
    if [ $? -eq 0]; then
        echo "Service $SERVICE_NAME started"
    else
        echo "Error starting service $SERVICE_NAME"
    fi
}

# Function to handle status
status_service() {
    check_service_file
    sudo systemctl status "$SERVICE_NAME"
}

# Function to handle stop
stop_service() {
    check_service_file
    sudo systemctl stop "$SERVICE_NAME"
    if [ $? -eq 0]; then
        echo "Service $SERVICE_NAME stopped"
    else
        echo "Error stopping service $SERVICE_NAME"
    fi
}

# Function to handle restart
restart_service() {
    check_service_file
    sudo systemctl restart "$SERVICE_NAME"
    if [ $? -eq 0]; then
        echo "Service $SERVICE_NAME restarted"
    else
        echo "Error restarting service $SERVICE_NAME"
    fi
}

# Main script logic
case "$1" in
    enable)
        enable_service
        ;;
    start)
        start_service
        ;;
    status)
        status_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    *)
        echo "Usage: $0 {enable|start|status|stop|restart}"
        exit 1
        ;;
esac

exit 0
