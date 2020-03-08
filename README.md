
# VIRTUAL MOUSE

## Prerequisite
    docker

## Run
Build a docker image

    sudo docker build -t virtual-mouse .
    
Run the container as 

    sudo docker run -d --rm -e DISPLAY --device=/dev/video0 --net=host virtual-mouse
To stop the container

    sudo docker stop $(sudo docker ps -q --filter ancestor=virtual-mouse)

## Description
Move red color object in front of the web-camera to move mouse cursor. Bring blue color object near red object to perform mouse left click event.

Note: Tested on ubuntu 16.04