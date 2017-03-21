# uniworx=/Users/changkun/Documents/Git/UniWorxMonitor
uniworx=/PATH/TO/YOUR/UniworXMonitor
cd $uniworx
found=false

if python main.py | grep -q new; then
    message="New Course Found! Check 'log.txt' for details..."
    found=true
else
    message="No Further Changes."
fi

osascript -e "display notification \" $message \" with title \"UniWorXMonitor\""

echo $found
if "$found" = true; then
    osascript -e "tell application \"Finder\" to open POSIX file \"$uniworx/log.txt\""
fi