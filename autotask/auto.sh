cd /PATH/TO/YOUR/UniWorxMonitor

if python main.py | grep new; then
    message="New Course Found! Check log.txt for details..."
else
    message="No Further Changes."
fi

osascript -e "display notification \" $message \" with title \"UniWorXMonitor\""
