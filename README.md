# dinogame
OpenCV toy project to create AI for the Chrome Dinosaur game. Current hiscore: 1773.

Uses OpenCV to scan for obstacles (birds and cacti). Depending on detection, the correct input (duck or jump) is given using PyAutoGui.
Speeding up of the game is monitored by counting the number of performed evasions. As a result:
 1. airtime during jumping is decreased;
 2. groundtime during ducking is decreased;
 3. the detection window shifts to the right to allow earlier detection of obstacles.
 
# Disclaimer
I cannot guarantee equal functioning on other hardware as:
 1. the detection bounding boxes are hardcoded and will likely only work on 1080p displays.
 2. image processing speed will differ depending on CPU/GPU.
