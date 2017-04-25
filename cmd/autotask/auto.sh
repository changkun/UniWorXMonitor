
# Configure the following path
# uniworx=/PATH/TO/YOUR/UniworXMonitor
# Example:
uniworx=/Users/changkun/Documents/Git/UniWorXMonitor

cd $uniworx
found=false

if python main.py | grep -q new; then
    message="New Course Found! Check 'log.txt' for details..."
    found=true
else
    message="No Further Changes."
fi

osascript -e "display notification \" $message \" with title \"UniWorXMonitor\""

if "$found" = true; then
    osascript -e "tell application \"Finder\" to open POSIX file \"$uniworx/log.txt\""
fi
