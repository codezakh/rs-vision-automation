#!/bin/bash

runeliteWindowId=`wmctrl -lG | grep -i runelite | cut -d ' ' -f 1`
eval `xdotool getwindowgeometry --shell $runeliteWindowId`
echo "\
x: $X
y: $Y
windowId: $runeliteWindowId
width: $WIDTH
height: $HEIGHT"
